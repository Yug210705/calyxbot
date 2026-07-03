import asyncio

from app.core.database import SessionLocal
from app.modules.search.services import VectorSearchService
from app.modules.search.embeddings import OpenAIEmbeddings

async def evaluate_retrieval():
    embedder = OpenAIEmbeddings()
    
    queries = [
        "What is the company budget for Q3?",
        "Engineering sprint planning details",
        "Who is John Smith?"
    ]
    
    print("--- Retrieval Evaluation ---")
    
    async with SessionLocal() as session:
        search_service = VectorSearchService(session, embedder)
        
        for q in queries:
            print(f"\nQuery: '{q}'")
            try:
                results = await search_service.search(
                    query=q, 
                    organization_id=None, # Will fail if org_id is required, we can grab a dummy org_id if needed
                    top_k=3
                )
                if not results:
                    print("  No results found. (Database might be empty or org_id needed)")
                for idx, r in enumerate(results):
                    print(f"  {idx+1}. [Score: {r['similarity_score']:.4f}] {r['document_title']}")
                    print(f"     Heading: {r.get('section_heading', 'None')}")
                    print(f"     Preview: {r['text'][:100]}...")
            except Exception as e:
                print(f"  Error running query: {e}")

if __name__ == "__main__":
    asyncio.run(evaluate_retrieval())
