from dataclasses import dataclass
from typing import Literal, List, Dict
import uuid

from app.modules.documents.models import DocumentChunk

@dataclass(frozen=True)
class ChunkReindexDecision:
    chunk_id: str
    action: Literal["keep", "reembed", "delete", "create"]
    reason: str

class ChunkReindexPlanner:
    def __init__(self, target_embedding_version: str):
        self.target_embedding_version = target_embedding_version

    def plan(
        self, 
        previous_chunks: List[DocumentChunk], 
        new_chunks: List[DocumentChunk]
    ) -> List[ChunkReindexDecision]:
        
        decisions: List[ChunkReindexDecision] = []
        prev_map: Dict[str, DocumentChunk] = {str(c.id): c for c in previous_chunks}
        new_map: Dict[str, DocumentChunk] = {str(c.id): c for c in new_chunks}

        # 1. Process all new chunks (either create or evaluate for re-embed/keep)
        for chunk_id, new_chunk in new_map.items():
            if chunk_id not in prev_map:
                decisions.append(ChunkReindexDecision(
                    chunk_id=chunk_id, 
                    action="create", 
                    reason="Chunk does not exist in previous state"
                ))
            else:
                prev_chunk = prev_map[chunk_id]
                
                # Evaluate if we need to re-embed
                reembed_reason = None
                
                if new_chunk.checksum != prev_chunk.checksum:
                    reembed_reason = "Checksum changed"
                elif new_chunk.section_heading != prev_chunk.section_heading:
                    reembed_reason = "Section heading changed"
                elif new_chunk.page_number != prev_chunk.page_number:
                    reembed_reason = "Page number changed"
                elif new_chunk.chunker_version != prev_chunk.chunker_version:
                    reembed_reason = "Chunker version changed"
                elif self.target_embedding_version != prev_chunk.embedding_version:
                    reembed_reason = "Target embedding version differs"
                elif not prev_chunk.embedding:
                    reembed_reason = "Missing embedding vector"
                    
                if reembed_reason:
                    decisions.append(ChunkReindexDecision(
                        chunk_id=chunk_id,
                        action="reembed",
                        reason=reembed_reason
                    ))
                else:
                    decisions.append(ChunkReindexDecision(
                        chunk_id=chunk_id,
                        action="keep",
                        reason="Chunk metadata and embeddings are up to date"
                    ))
                    
        # 2. Process old chunks that no longer exist
        for chunk_id in prev_map:
            if chunk_id not in new_map:
                decisions.append(ChunkReindexDecision(
                    chunk_id=chunk_id,
                    action="delete",
                    reason="Chunk no longer exists in current sync"
                ))
                
        return decisions
