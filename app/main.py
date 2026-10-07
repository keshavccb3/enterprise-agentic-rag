from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from app.core.config import settings
from app.services.chat import retriever, initialize, chat

app = FastAPI(title="Enterprise Agentic Knowledge Assistant", version="1.0.0")

class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    session_id: str = "default"
class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=10)
class EvaluateRequest(BaseModel):
    query: str = Field(min_length=1)
    expected_keywords: list[str] = []
    session_id: str = "evaluation"

@app.on_event("startup")
def startup(): initialize()

@app.get("/health")
def health():
    return {"status": "ok", "indexed_chunks": len(retriever.records), "model": settings.ollama_model}

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".txt", ".md", ".pdf"}:
        raise HTTPException(status_code=400, detail="Only TXT, MD and PDF files are supported.")
    target = Path(settings.data_dir) / Path(file.filename).name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(await file.read())
    return {"status": "indexed", "file": target.name, "indexed_chunks": retriever.rebuild()}

@app.post("/search")
def search(request: SearchRequest):
    return {"query": request.query, "results": retriever.search(request.query, request.top_k)}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return {"query": request.query, "session_id": request.session_id, **chat(request.query, request.session_id)}

@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    result = chat(request.query, request.session_id)
    answer = result["answer"].lower()
    matched = [k for k in request.expected_keywords if k.lower() in answer]
    score = len(matched) / len(request.expected_keywords) if request.expected_keywords else 0.0
    return {"score": round(score, 3), "matched_keywords": matched, "expected_keywords": request.expected_keywords, "answer": result["answer"], "route": result["route"]}
