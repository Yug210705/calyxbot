import os
from unittest import mock

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


def test_settings_validation_error_on_missing_required():
    """Test that missing required env vars raises a ValidationError."""
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)

        errors = exc_info.value.errors()
        error_fields = [error["loc"][0] for error in errors]

        # Verify that all required fields are reported as missing
        assert "SUPABASE_URL" in error_fields
        assert "SUPABASE_SERVICE_ROLE_KEY" in error_fields
        assert "SUPABASE_JWT_SECRET" in error_fields
        assert "DATABASE_URL" in error_fields


def test_settings_loads_valid_configuration():
    """Test that valid configuration loads correctly."""
    valid_env = {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "test-key",
        "SUPABASE_JWT_SECRET": "test-secret",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
        "APP_ENV": "staging",
        "LOG_LEVEL": "DEBUG"
    }

    with mock.patch.dict(os.environ, valid_env, clear=True):
        settings = Settings(_env_file=None)
        assert settings.SUPABASE_URL == "https://test.supabase.co"
        assert settings.APP_ENV == "staging"
        assert settings.LOG_LEVEL == "DEBUG"
        assert settings.CORS_ORIGINS == ["http://localhost:3000"] # Check default


def test_get_settings_is_cached():
    """Test that get_settings returns the same cached instance."""
    valid_env = {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "test-key",
        "SUPABASE_JWT_SECRET": "test-secret",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
    }
    with mock.patch.dict(os.environ, valid_env, clear=True):
        # Clear the cache first to ensure a clean state
        get_settings.cache_clear()

        settings_1 = get_settings()
        settings_2 = get_settings()

        assert settings_1 is settings_2
