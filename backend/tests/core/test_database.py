import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

@pytest.mark.asyncio
async def test_get_db_yields_session():
    """Test that get_db yields an AsyncSession and closes it."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.return_value = mock_session
    
    # We patch the session maker in the database module
    with patch("app.core.database.AsyncSessionLocal", return_value=mock_session):
        # We manually iterate the async generator
        db_gen = get_db()
        session = await anext(db_gen)
        
        assert session is mock_session
        
        # Finish the generator
        try:
            await anext(db_gen)
        except StopAsyncIteration:
            pass
            
        # Verify close was called (by context manager)
        # SQLAlchemy AsyncSession.__aexit__ calls close()
        mock_session.__aexit__.assert_awaited_once()
        mock_session.commit.assert_not_called()
        mock_session.rollback.assert_not_called()

@pytest.mark.asyncio
async def test_get_db_cleans_up_on_exception():
    """Test that get_db cleans up the session if an exception occurs."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.return_value = mock_session
    
    with patch("app.core.database.AsyncSessionLocal", return_value=mock_session):
        db_gen = get_db()
        session = await anext(db_gen)
        
        assert session is mock_session
        
        # Simulate an exception in the route handler by throwing into the generator
        test_exception = ValueError("Test error in route handler")
        
        with pytest.raises(ValueError, match="Test error in route handler"):
            await db_gen.athrow(test_exception)
            
        # Verify close was called (by context manager)
        mock_session.__aexit__.assert_awaited_once()
        mock_session.commit.assert_not_called()
