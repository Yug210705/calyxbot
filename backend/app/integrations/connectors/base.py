import abc
import uuid
from typing import AsyncGenerator, Dict, Any, List

class BaseConnector(abc.ABC):
    """Abstract base class for all external knowledge connectors."""

    @classmethod
    @abc.abstractmethod
    def provider_name(cls) -> str:
        """Return the unique provider name (e.g. 'google_drive', 'slack')."""
        pass

    @abc.abstractmethod
    async def get_health(self) -> bool:
        """Check if the connector can successfully authenticate and reach the provider API."""
        pass

    @abc.abstractmethod
    async def discover(self, sync_cursor: str = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Discover documents that need to be synced.
        Yields lightweight metadata items (e.g. file IDs, names, timestamps).
        """
        pass

    @abc.abstractmethod
    async def download(self, document_metadata: Dict[str, Any]) -> bytes:
        """
        Download the raw content for a single discovered document.
        """
        pass

    @abc.abstractmethod
    async def normalize(self, document_metadata: Dict[str, Any], raw_content: bytes) -> Dict[str, Any]:
        """
        Normalize the raw content into a standard plain text or markdown structure.
        Returns a dictionary containing 'title', 'content', 'mime_type', 'source', 'metadata'.
        """
        pass
