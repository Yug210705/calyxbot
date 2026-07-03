import re

def extract_snippet(text: str, query: str, window_before: int = 120, window_after: int = 180) -> str:
    """
    Extracts a query-aware snippet from a large chunk of text.
    If the query (or a token from it) is found, it centers the snippet around the match.
    Otherwise, it returns the first N characters as a fallback.
    """
    if not text:
        return ""
        
    if not query:
        return _format_fallback(text, window_before + window_after)
        
    # Normalize query into tokens for simple matching (case insensitive)
    # We'll just look for the first significant word (length >= 3) or just the first word
    query_tokens = [t.lower() for t in re.split(r'\W+', query) if t]
    
    # Try to find the whole query string first
    text_lower = text.lower()
    query_lower = query.lower()
    
    match_pos = text_lower.find(query_lower)
    
    # If not found, try finding the first token
    if match_pos == -1 and query_tokens:
        for token in query_tokens:
            if len(token) < 3:  # Skip very short words like 'is', 'a'
                continue
            pos = text_lower.find(token)
            if pos != -1:
                match_pos = pos
                break
                
    if match_pos == -1:
        # Fallback to first N chars
        return _format_fallback(text, window_before + window_after)
        
    # We found a match, extract a window around it
    start_pos = max(0, match_pos - window_before)
    end_pos = min(len(text), match_pos + window_after)
    
    # Try to align to word boundaries
    if start_pos > 0:
        # Find the next space to avoid cutting a word in half
        space_pos = text.find(' ', start_pos)
        if space_pos != -1 and space_pos < match_pos:
            start_pos = space_pos + 1
            
    if end_pos < len(text):
        # Find the last space before end_pos
        space_pos = text.rfind(' ', match_pos, end_pos)
        if space_pos != -1 and space_pos > match_pos:
            end_pos = space_pos
            
    snippet = text[start_pos:end_pos].strip()
    
    if start_pos > 0:
        snippet = "..." + snippet
    if end_pos < len(text):
        snippet = snippet + "..."
        
    return snippet

def _format_fallback(text: str, max_len: int) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    
    # Find last space within max_len to avoid word cut
    space_pos = text.rfind(' ', 0, max_len)
    if space_pos != -1:
        return text[:space_pos] + "..."
    return text[:max_len] + "..."
