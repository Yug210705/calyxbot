"""User and Membership database models."""

import uuid

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.models import Base, TimestampMixin


class User(Base, TimestampMixin):
    """
    Calyx User model.
    Note: The Supabase auth.users table handles password hashing, 2FA, and SSO.
    This table stores the application-level user profile. The ID here matches the Supabase User ID.
    """
    __tablename__ = "users"

    # id matches Supabase auth.users.id
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
