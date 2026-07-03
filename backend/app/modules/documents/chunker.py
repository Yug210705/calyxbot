import hashlib
import re
from dataclasses import dataclass

from app.modules.documents.tokenizer import Tokenizer

@dataclass(frozen=True)
class ChunkingConfig:
    max_tokens: int
    overlap_tokens: int
    separators: list[str]
    preserve_headings: bool
    preserve_pages: bool

@dataclass(frozen=True)
class HeadingContext:
    levels: tuple[str, ...] = ()
    
    @property
    def hierarchy_str(self) -> str | None:
        return " > ".join(self.levels) if self.levels else None

@dataclass(frozen=True)
class HeadingInfo:
    level: int
    text: str

@dataclass
class ChunkResult:
    text: str
    index: int
    token_count: int
    start_offset: int
    end_offset: int
    checksum: str
    language: str = "unknown"
    page_number: int | None = None
    section_heading: str | None = None
    chunker_version: str = "1.1"

def is_page_break(piece: str) -> bool:
    return "\f" in piece

def extract_heading(piece: str) -> HeadingInfo | None:
    match = re.match(r"^(#{1,6})\s+(.*)$", piece.strip())
    if match:
        return HeadingInfo(level=len(match.group(1)), text=match.group(2).strip())
    return None

def is_hard_boundary_transition(has_body_content: bool, piece: str) -> bool:
    """Returns True if the piece introduces a boundary that should force a flush of the current buffer."""
    if is_page_break(piece):
        return True
    if has_body_content and extract_heading(piece) is not None:
        return True
    return False

class RecursiveChunker:
    """An enterprise-grade recursive chunker supporting overlaps, semantic boundaries, and metadata preservation."""
    CHUNKER_VERSION = "1.1"
    
    def __init__(self, tokenizer: Tokenizer, config: ChunkingConfig):
        self.tokenizer = tokenizer
        self.config = config

    def _get_checksum(self, doc_checksum: str, text: str, start_offset: int, end_offset: int) -> str:
        # Checksum should not depend on chunk index
        base = f"{doc_checksum}_{text}_{start_offset}_{end_offset}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

    def _update_heading_dict(self, current_headings: dict[int, str], heading: HeadingInfo) -> dict[int, str]:
        new_headings = current_headings.copy()
        keys_to_delete = [k for k in new_headings.keys() if k >= heading.level]
        for k in keys_to_delete:
            del new_headings[k]
        new_headings[heading.level] = heading.text
        return new_headings

    def _build_heading_context(self, current_headings: dict[int, str]) -> HeadingContext:
        sorted_levels = sorted(current_headings.keys())
        return HeadingContext(tuple(current_headings[l] for l in sorted_levels))

    def chunk_document(self, text: str, document_checksum: str) -> list[ChunkResult]:
        if not text:
            return []

        chunks = []
        current_headings: dict[int, str] = {}
        current_page = 1
        
        def _split_recursively(sub_text: str, offset: int, cur_headings: dict[int, str], cur_page: int, allowed_separators: list[str]) -> list[tuple[str, int, dict[int, str], int]]:
            token_len = self.tokenizer.count_tokens(sub_text)
            
            must_split = False
            if self.config.preserve_headings and "\n#" in sub_text:
                must_split = True
            if self.config.preserve_headings and sub_text.startswith("#"):
                must_split = True
            if self.config.preserve_pages and "\f" in sub_text:
                must_split = True
                
            if token_len <= self.config.max_tokens and not must_split:
                return [(sub_text, offset, cur_headings.copy(), cur_page)]
                
            for sep_idx, separator in enumerate(allowed_separators):
                if separator == "":
                    return [(c, offset + i, cur_headings.copy(), cur_page) for i, c in enumerate(sub_text)]
                
                parts = sub_text.split(separator)
                if len(parts) > 1:
                    if all(p + separator == sub_text or p == sub_text for p in parts):
                        continue
                        
                    result = []
                    current_offset = offset
                    local_headings = cur_headings.copy()
                    local_page = cur_page
                    
                    for i, part in enumerate(parts):
                        actual_part = part if i == len(parts) - 1 else part + separator
                        if not actual_part:
                            continue
                            
                        if self.config.preserve_headings:
                            heading = extract_heading(actual_part)
                            if heading:
                                local_headings = self._update_heading_dict(local_headings, heading)
                                
                        if self.config.preserve_pages:
                            if "\f" in actual_part:
                                local_page += actual_part.count("\f")
                                
                        next_separators = allowed_separators[sep_idx:] if actual_part != sub_text else allowed_separators[sep_idx + 1:]
                        sub_results = _split_recursively(actual_part, current_offset, local_headings, local_page, next_separators)
                        result.extend(sub_results)
                        current_offset += len(actual_part)
                        
                    return result
            
            return [(sub_text, offset, cur_headings.copy(), cur_page)]

        atomic_pieces = _split_recursively(text, 0, current_headings, current_page, self.config.separators)
        
        def flush_buffer(buf: list[tuple[str, int, dict[int, str], int]], index: int) -> ChunkResult | None:
            if not buf:
                return None
            first_piece = buf[0]
            last_piece = buf[-1]
            heading_ctx = self._build_heading_context(last_piece[2])
            page_num = first_piece[3] if self.config.preserve_pages else None
            
            full_text = "".join(p[0] for p in buf).replace("\f", "")
            chunk_text = full_text.strip()
            
            if not chunk_text:
                return None
                
            raw_full_text = "".join(p[0] for p in buf)
            start_diff = len(raw_full_text) - len(raw_full_text.lstrip())
            c_start = first_piece[1] + start_diff
            c_end = c_start + len(chunk_text)
            
            return ChunkResult(
                text=chunk_text,
                index=index,
                token_count=self.tokenizer.count_tokens(chunk_text),
                start_offset=c_start,
                end_offset=c_end,
                checksum=self._get_checksum(document_checksum, chunk_text, c_start, c_end),
                language="unknown",
                page_number=page_num,
                section_heading=heading_ctx.hierarchy_str,
                chunker_version=self.CHUNKER_VERSION
            )

        merged_chunks = []
        buffer: list[tuple[str, int, dict[int, str], int]] = []
        current_tokens = 0
        chunk_index = 0
        has_body_content = False
        
        for piece_text, piece_offset, piece_headings, piece_page in atomic_pieces:
            piece_tokens = self.tokenizer.count_tokens(piece_text)
            
            if buffer:
                is_boundary = False
                if (self.config.preserve_pages and piece_page != buffer[-1][3]) or (self.config.preserve_headings and is_hard_boundary_transition(has_body_content, piece_text)):
                    is_boundary = True
                    
                if is_boundary or (current_tokens + piece_tokens > self.config.max_tokens):
                    chunk_res = flush_buffer(buffer, chunk_index)
                    if chunk_res:
                        merged_chunks.append(chunk_res)
                        chunk_index += 1
                        
                    overlap_buffer = []
                    overlap_tokens = 0
                    if not is_boundary:
                        for p in reversed(buffer):
                            p_toks = self.tokenizer.count_tokens(p[0])
                            if overlap_tokens + p_toks <= self.config.overlap_tokens:
                                overlap_buffer.insert(0, p)
                                overlap_tokens += p_toks
                            else:
                                break
                    buffer = overlap_buffer
                    current_tokens = overlap_tokens
                    has_body_content = False

            buffer.append((piece_text, piece_offset, piece_headings, piece_page))
            current_tokens += piece_tokens
            
            if not is_page_break(piece_text) and not extract_heading(piece_text) and piece_text.strip():
                has_body_content = True
                
        if buffer:
            chunk_res = flush_buffer(buffer, chunk_index)
            if chunk_res:
                merged_chunks.append(chunk_res)

        return merged_chunks
