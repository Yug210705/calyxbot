import pytest
import asyncio
from app.shared.events import InProcessEventBus, DomainEvent

@pytest.mark.asyncio
async def test_event_bus_fault_tolerance():
    bus = InProcessEventBus()
    
    # We will subscribe two handlers
    # The first will raise an exception
    # The second should still execute and succeed.
    
    execution_order = []
    
    async def failing_handler(event: DomainEvent) -> None:
        execution_order.append("failing")
        raise ValueError("I am a simulated failure")
        
    async def succeeding_handler(event: DomainEvent) -> None:
        execution_order.append("succeeding")
        
    bus.subscribe("test.event", failing_handler)
    bus.subscribe("test.event", succeeding_handler)
    
    event = DomainEvent(name="test.event", payload={"data": 123})
    
    # The publish should NOT raise the ValueError
    await bus.publish(event)
    
    # Both handlers should have been executed in order
    assert execution_order == ["failing", "succeeding"]
