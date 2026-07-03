import logging
from typing import Any
from collections.abc import Callable, Awaitable

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable[[dict[str, Any]], Awaitable[None]]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[dict[str, Any]], Awaitable[None]]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, payload: dict[str, Any]):
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(payload)
            except Exception as e:
                logger.error(f"Error handling event {event_type}: {e}")

# Global singleton for in-process EventBus
event_bus = EventBus()
