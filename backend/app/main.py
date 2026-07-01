"""Calyx API application factory.

Creates and configures the FastAPI application instance. All middleware,
exception handlers, and module routers are registered through this factory.

Usage:
    uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, APIRouter
from sqlalchemy import text

from app.core.database import engine
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import RequestIDAndLoggingMiddleware
from app.shared.events import event_bus
from app.modules.audit.services import AuditLogService
from app.core.exceptions import register_exception_handlers

# Ensure all models are imported so SQLAlchemy metadata is fully populated
from app.modules.auth.models import User
from app.modules.organizations.models import Organization
from app.modules.members.models import Membership, Role, Permission, RolePermission
from app.modules.members.invitation_models import Invitation
from app.modules.audit.models import AuditLog

# Setup logging immediately so everything during startup uses structlog
setup_logging("INFO")

logger = logging.getLogger(__name__)
settings = get_settings()

APP_TITLE = "Calyx API"
APP_DESCRIPTION = (
    "Enterprise Memory Operating System "
    "— Preserve organizational knowledge."
)
APP_VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Setup structured logging
    setup_logging(log_level=settings.LOG_LEVEL)
    logger.info("Starting Calyx API...", env=settings.APP_ENV)
    
    # Initialize background services
    audit_service = AuditLogService(event_bus)
    audit_service.setup_subscriptions()
    
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.critical(f"Failed to connect to the database: {e}")
        raise RuntimeError("Database connection failed on startup") from e
    
    yield
    
    logger.info("Shutting down Calyx API...")
    await engine.dispose()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    This factory constructs the application and registers all components
    in the correct order:

    1. Core middleware (request ID, CORS, logging)
    2. Exception handlers
    3. Module routers

    Each registration step is encapsulated in a private function so that
    future tickets can extend the factory without modifying existing code.

    Returns:
        A fully configured FastAPI application instance.
    """
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    _register_middleware(app)
    _register_exceptions(app)
    _register_routes(app)

    return app

def _register_middleware(app: FastAPI) -> None:
    """Register application middlewares."""
    app.add_middleware(RequestIDAndLoggingMiddleware)

def _register_exceptions(app: FastAPI) -> None:
    """Register global exception handlers."""
    register_exception_handlers(app)

def _register_routes(app: FastAPI) -> None:
    """Register application-level routes.
    Modules should expose their own APIRouters.
    """
    from app.modules.auth.routes import router as auth_router
    from app.modules.organizations.router import router as org_router
    from app.modules.members.invitation_router import router as invitation_router

    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(auth_router)
    api_router.include_router(org_router)
    api_router.include_router(invitation_router)
    
    app.include_router(api_router)

    @app.get(
        "/",
        summary="Service Root",
        description="Returns service identification and status.",
        tags=["System"],
        response_description="Service identification payload",
    )
    async def root() -> dict[str, str]:
        """Return service identification and health status."""
        return {
            "status": "ok",
            "service": "calyx-api",
            "version": APP_VERSION,
        }


app = create_app()
