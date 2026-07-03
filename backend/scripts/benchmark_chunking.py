import time
import tracemalloc
from app.modules.documents.chunker import RecursiveChunker, ChunkingConfig
from app.modules.documents.tokenizer import Tokenizer

def run_benchmark():
    tokenizer = Tokenizer()
    config = ChunkingConfig(
        max_tokens=500,
        overlap_tokens=50,
        separators=["\n# ", "\n## ", "\n### ", "\n\n", "\n", ". ", " "],
        preserve_headings=True,
        preserve_pages=True
    )
    chunker = RecursiveChunker(tokenizer, config)

    # Generate dummy texts of roughly 100KB, 1MB, 10MB
    # Let's say average word is 5 bytes + space = 6 bytes.
    # 100KB = ~17,000 words.
    
    base_paragraph = "# Benchmark Header\n\nThis is a benchmark paragraph. It is not very long but it serves the purpose of being repeated over and over again to build up the necessary file sizes for the benchmark tests. We will use it extensively.\n\n## Subheading\n\nAnother paragraph under a subheading. This should trigger semantic boundaries."
    
    sizes_kb = [100, 1000, 10000]
    
    print(f"{'Size (KB)':<10} | {'Chunks':<8} | {'Time (s)':<10} | {'Tokens/sec':<12} | {'Mem (MB)':<10}")
    print("-" * 60)
    
    for size in sizes_kb:
        target_bytes = size * 1024
        
        # Build text
        repeats = target_bytes // len(base_paragraph.encode('utf-8'))
        text = "\n\n".join([base_paragraph] * repeats)
        
        # Count tokens once
        num_tokens = tokenizer.count_tokens(text)
        
        # Benchmark
        tracemalloc.start()
        start_time = time.time()
        
        chunks = chunker.chunk_document(text, "dummy_checksum")
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        elapsed = end_time - start_time
        tokens_per_sec = num_tokens / elapsed if elapsed > 0 else 0
        peak_mb = peak / (1024 * 1024)
        
        print(f"{size:<10} | {len(chunks):<8} | {elapsed:<10.4f} | {tokens_per_sec:<12.2f} | {peak_mb:<10.2f}")

if __name__ == "__main__":
    run_benchmark()
