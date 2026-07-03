import pytest
from app.modules.documents.tokenizer import Tokenizer
from app.modules.documents.chunker import RecursiveChunker, ChunkingConfig, ChunkResult

def test_page_break_forces_new_chunk():
    tokenizer = Tokenizer()
    config = ChunkingConfig(
        max_tokens=500, # Large limit so token size doesn't force split
        overlap_tokens=10, 
        separators=["\n\n", "\n", " "],
        preserve_headings=True,
        preserve_pages=True
    )
    chunker = RecursiveChunker(tokenizer, config)
    
    text = "Page 1 content\n\n\f\n\nPage 2 content"
    chunks = chunker.chunk_document(text, "mock_checksum")
    
    # 2 chunks minimum if content spans \f
    assert len(chunks) == 2
    # no chunk contains \f
    for c in chunks:
        assert "\f" not in c.text
    # page numbers split correctly
    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 2
    # chunk 1 page != chunk 2 page
    assert chunks[0].page_number != chunks[1].page_number

def test_heading_transition_forces_new_chunk():
    tokenizer = Tokenizer()
    config = ChunkingConfig(
        max_tokens=500,
        overlap_tokens=10,
        separators=["\n\n", "\n"],
        preserve_headings=True,
        preserve_pages=False
    )
    chunker = RecursiveChunker(tokenizer, config)
    
    text = "# Company\n\nbody text 1\n\n# HR\n\nbody text 2"
    chunks = chunker.chunk_document(text, "mock_checksum")
    
    assert len(chunks) == 2
    assert chunks[0].section_heading == "Company"
    assert chunks[1].section_heading == "HR"
    assert "body text 1" in chunks[0].text
    assert "body text 2" in chunks[1].text
    assert "body text 2" not in chunks[0].text
    assert "body text 1" not in chunks[1].text

def test_nested_heading_hierarchy_propagates():
    tokenizer = Tokenizer()
    config = ChunkingConfig(
        max_tokens=500,
        overlap_tokens=10,
        separators=["\n\n", "\n"],
        preserve_headings=True,
        preserve_pages=False
    )
    chunker = RecursiveChunker(tokenizer, config)
    
    text = "# Company\n\n## Engineering\n\n### Sprint Planning\n\nThe planning body"
    chunks = chunker.chunk_document(text, "mock_checksum")
    
    assert len(chunks) == 1
    assert chunks[0].section_heading == "Company > Engineering > Sprint Planning"

def test_overlap_preserved_without_cross_boundary_contamination():
    tokenizer = Tokenizer()
    config = ChunkingConfig(
        max_tokens=10, 
        overlap_tokens=5, 
        separators=["\n\n", "\n", " "],
        preserve_headings=True,
        preserve_pages=True
    )
    chunker = RecursiveChunker(tokenizer, config)
    
    text = "Word1 word2 word3 word4 word5 word6 word7\n\n\f\n\nWord8 word9 word10 word11"
    chunks = chunker.chunk_document(text, "mock_checksum")
    
    # Check page boundaries are respected
    page1_chunks = [c for c in chunks if c.page_number == 1]
    page2_chunks = [c for c in chunks if c.page_number == 2]
    
    assert len(page1_chunks) > 0
    assert len(page2_chunks) > 0
    
    for c in page1_chunks:
        assert "Word8" not in c.text # Overlap must not grab from next page
        
    for c in page2_chunks:
        assert "Word7" not in c.text # Overlap must not grab from prev page
