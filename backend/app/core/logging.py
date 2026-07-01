"""Structured logging configuration.

Configures structlog for JSON-formatted log output with contextual fields
(request_id, user_id, org_id) automatically attached to every log entry.
"""

import logging
import sys
from contextvars import ContextVar

import structlog

# Context variables for request-bound attributes
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
org_id_var: ContextVar[str] = ContextVar("org_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


def _add_context_vars(logger: logging.Logger, method_name: str, event_dict: dict) -> dict:
    """Structlog processor to inject contextual data into log lines."""
    req_id = request_id_var.get()
    if req_id:
        event_dict["request_id"] = req_id

    org_id = org_id_var.get()
    if org_id:
        event_dict["org_id"] = org_id

    user_id = user_id_var.get()
    if user_id:
        event_dict["user_id"] = user_id

    correlation_id = correlation_id_var.get()
    if correlation_id:
        event_dict["correlation_id"] = correlation_id

    return event_dict


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging using structlog."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            _add_context_vars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def increment_counter(metric_name: str, value: int = 1, tags: dict = None) -> None:
    """
    Emit a metric to the logs.
    
    This structured log can be scraped by Promtail/FluentBit and 
    converted into Prometheus counters automatically.
    """
    logger = structlog.get_logger("metrics")
    event_dict = {
        "metric_type": "counter",
        "metric_name": metric_name,
        "value": value
    }
    if tags:
        event_dict.update(tags)

    logger.info("metric", **event_dict)
