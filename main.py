from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import get_research_answer
from openrouter_client import openrouter_query
from gemini_client import gemini_query

app = FastAPI()

# --- DB Size Endpoint ---
@app.get("/db_size")
def db_size():
    try:
        if 'vectorstore' in globals() and vectorstore is not None:
            return {"size": len(vectorstore.docstore._dict)}
        else:
            return {"size": 0}
    except Exception:
        return {"size": 0}

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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