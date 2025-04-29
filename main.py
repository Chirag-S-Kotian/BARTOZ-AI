from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import get_research_answer, vectorstore
from data_sources_config import AI_SOURCES
import os
from openrouter_client import openrouter_query
from gemini_client import gemini_query

app = FastAPI()

# --- Async ingestion at startup ---
@app.on_event("startup")
async def ingest_async_resources():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    import os
    from async_ingest import fetch_and_ingest_async_resources
    global vectorstore
    faiss_index_path = "faiss_index"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Load or create vectorstore
    if os.path.exists(faiss_index_path):
        vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents([], embeddings)
    await fetch_and_ingest_async_resources(vectorstore)

# --- Health Endpoint ---
@app.get("/health")
def health():
    return {"status": "ok"}

# --- Model Health Endpoint ---
@app.get("/model_health")
def model_health():
    import requests
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models"
    openrouter_url = "https://openrouter.ai/api/v1/models"
    out = {}
    try:
        resp = requests.get(gemini_url, timeout=6)
        if resp.status_code == 200:
            out['gemini'] = {"status": "ok", "error": ""}
        else:
            out['gemini'] = {"status": "error", "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        out['gemini'] = {"status": "error", "error": str(e)}
    try:
        resp = requests.get(openrouter_url, timeout=6)
        if resp.status_code == 200:
            out['openrouter'] = {"status": "ok", "error": ""}
        else:
            out['openrouter'] = {"status": "error", "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        out['openrouter'] = {"status": "error", "error": str(e)}
    return out

# --- Sources Endpoint ---
@app.get("/sources")
def sources():
    # List all sources: static and pluggable
    static_sources = ["arxiv", "pubmed", "ssrn", "ai_companies"]
    dynamic_sources = [src['name'] for src in AI_SOURCES]
    return {"static_sources": static_sources, "dynamic_sources": dynamic_sources}

# --- DB Size Endpoint ---
@app.get("/db_size")
def db_size():
    try:
        # Always reload vectorstore if not loaded
        global vectorstore
        if vectorstore is None:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            faiss_index_path = "faiss_index"
            if os.path.exists(faiss_index_path):
                vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
        if vectorstore is not None:
            return {"size": len(vectorstore.docstore._dict)}
        else:
            return {"size": 0}
    except Exception as e:
        print(f"Error in /db_size: {e}")
        return {"size": 0}

# --- Docs Preview Endpoint ---
@app.get("/docs_preview")
def docs_preview():
    try:
        global vectorstore
        if vectorstore is None:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            faiss_index_path = "faiss_index"
            if os.path.exists(faiss_index_path):
                vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
        if vectorstore is not None:
            docs = list(vectorstore.docstore._dict.values())[:10]
            preview = []
            for doc in docs:
                preview.append({
                    "title": doc.metadata.get("title", "N/A"),
                    "summary": doc.page_content[:200],
                    "source": doc.metadata.get("source", "N/A"),
                    "published_date": doc.metadata.get("published_date", "N/A"),
                    "url": doc.metadata.get("url", "N/A")
                })
            return {"preview": preview}
        else:
            return {"preview": []}
    except Exception as e:
        print(f"Error in /docs_preview: {e}")
        return {"preview": []}

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

class QueryRequest(BaseModel):
    query: str
    model: str

@app.post("/query")
async def query_route(request: QueryRequest):
    try:
        response = await get_research_answer(request.query, request.model)
        return {"response": response}
    except Exception as e:
        # Log the exact error (optional for debug)
        print(f"Error while processing query: {str(e)}")
        # Return proper HTTP error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")