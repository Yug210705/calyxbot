import abc
import asyncio
import logging
from typing import List
from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APITimeoutError, InternalServerError
from app.core.config import get_settings

logger = logging.getLogger(__name__)

class EmbeddingInterface(abc.ABC):
    @abc.abstractproperty
    def vector_size(self) -> int:
        """Return the dimensionality of the embeddings generated."""
        pass

    @abc.abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document chunks."""
        pass

    @abc.abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        pass

class OpenAIEmbeddings(EmbeddingInterface):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=getattr(settings, "OPENAI_API_KEY", "dummy"))
        self._vector_size = 1536 if "small" in model else 3072

    @property
    def vector_size(self) -> int:
        return self._vector_size

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        retries = 3
        backoff = 1.0
        
        for attempt in range(retries):
            try:
                # Call OpenAI batch API
                response = await self.client.embeddings.create(
                    input=texts,
                    model=self.model
                )
                # Ensure ordered returns
                response.data.sort(key=lambda x: x.index)
                return [item.embedding for item in response.data]
            except (APIConnectionError, RateLimitError, APITimeoutError, InternalServerError) as e:
                if attempt == retries - 1:
                    logger.error(f"Failed to embed documents after {retries} attempts: {e}")
                    raise
                logger.warning(f"Transient error from OpenAI ({e}), retrying in {backoff}s...")
                await asyncio.sleep(backoff)
                backoff *= 2

    async def embed_query(self, text: str) -> List[float]:
        docs = await self.embed_documents([text])
        return docs[0]
