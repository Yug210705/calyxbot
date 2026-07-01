import abc
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

@dataclass
class DomainEvent:
    name: str
    payload: dict[str, Any]

class EventBus(abc.ABC):
    @abc.abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass

    @abc.abstractmethod
    def subscribe(self, event_name: str, handler: Callable[[DomainEvent], Awaitable[None]]) -> None:
        pass

class InProcessEventBus(EventBus):
    def __init__(self):
        self._handlers: dict[str, list[Callable[[DomainEvent], Awaitable[None]]]] = {}

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                # We await them in-process, but wrap in a try-except to ensure
                # listener failure does not rollback the main transaction.
                await handler(event)
            except Exception as e:
                logger.exception(
                    "Event handler failed",
                    event_name=event.name,
                    handler=handler.__name__,
                    error=str(e)
                )

    def subscribe(self, event_name: str, handler: Callable[[DomainEvent], Awaitable[None]]) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

# Global singleton for simplicity in MVP, injected where needed
event_bus = InProcessEventBus()
