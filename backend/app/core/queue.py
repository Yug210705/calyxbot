import abc
import asyncio
import logging
from typing import Any
from collections.abc import Callable, Awaitable

logger = logging.getLogger(__name__)

class RetryableError(Exception):
    """Exception indicating the task should be retried (e.g. 429, 503, network timeout)."""
    pass

class NonRetryableError(Exception):
    """Exception indicating the task should fail immediately (e.g. 401, 403, 404, bad payload)."""
    pass

class TaskQueue(abc.ABC):
    @abc.abstractmethod
    async def enqueue(self, task_type: str, payload: dict[str, Any]) -> str:
        pass

    @abc.abstractmethod
    def register_worker(self, task_type: str, handler: Callable[[dict[str, Any]], Awaitable[None]]):
        pass
        
    @abc.abstractmethod
    async def start_processing(self):
        pass

    @abc.abstractmethod
    async def stop_processing(self):
        pass

class InMemoryQueue(TaskQueue):
    def __init__(self, max_retries: int = 3):
        self.queue = asyncio.Queue()
        self.dead_letter_queue = asyncio.Queue()
        self.handlers: dict[str, Callable[[dict[str, Any]], Awaitable[None]]] = {}
        self._worker_tasks = []
        self.max_retries = max_retries

    async def enqueue(self, task_type: str, payload: dict[str, Any], attempt: int = 1) -> str:
        task_id = f"mem-{id(payload)}-{attempt}"
        await self.queue.put({
            "task_id": task_id, 
            "type": task_type, 
            "payload": payload,
            "attempt": attempt
        })
        return task_id

    async def _send_to_dlq(self, task: dict[str, Any], reason: str):
        logger.error(f"Task {task['task_id']} sent to DLQ. Reason: {reason}")
        task["dlq_reason"] = reason
        await self.dead_letter_queue.put(task)

    def register_worker(self, task_type: str, handler: Callable[[dict[str, Any]], Awaitable[None]]):
        self.handlers[task_type] = handler

    async def start_processing(self, concurrency: int = 1):
        if not self._worker_tasks:
            for _ in range(concurrency):
                task = asyncio.create_task(self._process_loop())
                self._worker_tasks.append(task)

    async def stop_processing(self):
        for task in self._worker_tasks:
            task.cancel()
        
        if self._worker_tasks:
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)
            self._worker_tasks.clear()

    async def _process_loop(self):
        while True:
            task = await self.queue.get()
            task_type = task["type"]
            handler = self.handlers.get(task_type)
            
            if not handler:
                logger.warning(f"No handler registered for task type: {task_type}")
                await self._send_to_dlq(task, "No handler registered")
                self.queue.task_done()
                continue
                
            try:
                await handler(task["payload"])
            except NonRetryableError as e:
                logger.error(f"Task {task['task_id']} failed with NonRetryableError: {e}")
                await self._send_to_dlq(task, f"NonRetryableError: {e}")
            except RetryableError as e:
                if task["attempt"] < self.max_retries:
                    logger.warning(f"Task {task['task_id']} failed with RetryableError, retrying (attempt {task['attempt'] + 1})")
                    await self.enqueue(task_type, task["payload"], task["attempt"] + 1)
                else:
                    logger.error(f"Task {task['task_id']} exhausted {self.max_retries} retries.")
                    await self._send_to_dlq(task, f"Max retries exhausted. Last error: {e}")
            except Exception as e:
                # Default unknown exceptions to DLQ to prevent poison pills
                logger.exception(f"Task {task['task_id']} encountered unexpected error.")
                await self._send_to_dlq(task, f"Unexpected error: {e}")
                
            self.queue.task_done()

# Global singleton for in-process queue
task_queue = InMemoryQueue()
