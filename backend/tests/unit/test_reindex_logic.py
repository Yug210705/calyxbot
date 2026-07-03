import uuid
import pytest
from app.modules.documents.models import DocumentChunk
from app.modules.documents.reindex import ChunkReindexPlanner

def build_chunk(**kwargs) -> DocumentChunk:
    # default test chunk
    base = {
        "id": uuid.uuid4(),
        "document_id": uuid.uuid4(),
        "index": 0,
        "text": "test text",
        "token_count": 2,
        "start_offset": 0,
        "end_offset": 9,
        "page_number": 1,
        "section_heading": "Test",
        "checksum": "chk123",
        "language": "en",
        "chunker_version": "1.1",
        "embedding_version": "v1",
        "source_document_version": 1,
        "chunk_hash": "testhash",
        "embedding": [0.1, 0.2]
    }
    base.update(kwargs)
    return DocumentChunk(**base)

def test_chunk_checksum_change_triggers_reembed():
    chunk_id = uuid.uuid4()
    prev_chunk = build_chunk(id=chunk_id, checksum="old_checksum")
    new_chunk = build_chunk(id=chunk_id, checksum="new_checksum")
    
    planner = ChunkReindexPlanner(target_embedding_version="v1")
    decisions = planner.plan([prev_chunk], [new_chunk])
    
    assert len(decisions) == 1
    assert decisions[0].action == "reembed"
    assert "Checksum" in decisions[0].reason

def test_section_heading_change_triggers_reembed():
    chunk_id = uuid.uuid4()
    prev_chunk = build_chunk(id=chunk_id, section_heading="Heading 1")
    new_chunk = build_chunk(id=chunk_id, section_heading="Heading 2")
    
    planner = ChunkReindexPlanner(target_embedding_version="v1")
    decisions = planner.plan([prev_chunk], [new_chunk])
    
    assert len(decisions) == 1
    assert decisions[0].action == "reembed"
    assert "Section heading" in decisions[0].reason

def test_page_number_change_triggers_reembed():
    chunk_id = uuid.uuid4()
    prev_chunk = build_chunk(id=chunk_id, page_number=1)
    new_chunk = build_chunk(id=chunk_id, page_number=2)
    
    planner = ChunkReindexPlanner(target_embedding_version="v1")
    decisions = planner.plan([prev_chunk], [new_chunk])
    
    assert len(decisions) == 1
    assert decisions[0].action == "reembed"
    assert "Page number" in decisions[0].reason

def test_document_version_change_alone_does_not_trigger_reembed():
    chunk_id = uuid.uuid4()
    prev_chunk = build_chunk(id=chunk_id, source_document_version=1)
    new_chunk = build_chunk(id=chunk_id, source_document_version=2)
    
    planner = ChunkReindexPlanner(target_embedding_version="v1")
    decisions = planner.plan([prev_chunk], [new_chunk])
    
    assert len(decisions) == 1
    assert decisions[0].action == "keep"

def test_embedding_version_change_triggers_reembed():
    chunk_id = uuid.uuid4()
    prev_chunk = build_chunk(id=chunk_id, embedding_version="v1")
    new_chunk = build_chunk(id=chunk_id)
    
    planner = ChunkReindexPlanner(target_embedding_version="v2")
    decisions = planner.plan([prev_chunk], [new_chunk])
    
    assert len(decisions) == 1
    assert decisions[0].action == "reembed"
    assert "Target embedding version" in decisions[0].reason
