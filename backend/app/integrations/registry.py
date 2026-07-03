from typing import ClassVar
from app.integrations.connectors.base import BaseConnector

class ConnectorRegistry:
    """Central registry for discovering and instantiating connectors."""
    
    _connectors: ClassVar[dict[str, type[BaseConnector]]] = {}

    @classmethod
    def register(cls, connector_cls: type[BaseConnector]) -> None:
        provider = connector_cls.provider_name()
        if provider in cls._connectors:
            raise ValueError(f"Connector for provider {provider} is already registered.")
        cls._connectors[provider] = connector_cls

    @classmethod
    def get_connector_class(cls, provider: str) -> type[BaseConnector]:
        if provider not in cls._connectors:
            raise ValueError(f"No connector registered for provider {provider}.")
        return cls._connectors[provider]

def initialize_registry():
    """Called at application startup to register all available plugins."""
    from app.integrations.connectors.google.connector import GoogleDriveConnector
    
    # Register connectors
    ConnectorRegistry.register(GoogleDriveConnector)
