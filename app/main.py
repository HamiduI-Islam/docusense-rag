from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Import our custom modules
from app.vector_store import retrieve_context
from app.llm_service import generate_grounded_response

class QueryRequest(BaseModel):
    question: str

class SourceNode(BaseModel):
    chunk_id: str
    similarity_score: float
    text_snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceNode]
    tokens_used: int

app = FastAPI(
    title="DocuSense RAG API",
    description="Lightweight Grounded RAG Service",
    version="1.0.0"
)

@app.post("/api/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """
    Receives a question, retrieves context, and synthesizes a grounded response.
    """
    try:
        # 1. Retrieve the top 3 most relevant chunks from ChromaDB
        search_results = retrieve_context(request.question, top_k=3)
        
        # 2. Extract the data for the LLM and the API response
        ids = search_results['ids'][0]
        distances = search_results['distances'][0]
        documents = search_results['documents'][0]
        
        # 3. Generate the answer using OpenAI
        answer, tokens_used = generate_grounded_response(request.question, documents)
        
        # 4. Format the source nodes for the API payload
        sources = []
        for idx in range(len(ids)):
            sources.append(
                SourceNode(
                    chunk_id=ids[idx],
                    similarity_score=round(distances[idx], 4),
                    # Provide a short 100-character snippet for the payload
                    text_snippet=documents[idx][:100] + "..." 
                )
            )
            
        # 5. Return the final structured response
        return QueryResponse(
            answer=answer,
            sources=sources,
            tokens_used=tokens_used
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}