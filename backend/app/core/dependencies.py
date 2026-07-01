"""Shared FastAPI dependencies.

Common dependencies used across multiple modules, including database session
management, current user resolution, and organization context.
"""

from app.core.database import get_db

__all__ = ["get_db"]
