# Enterprise Agentic Knowledge Assistant

A from-scratch Agentic RAG backend built with Python, LangGraph, LangChain, FAISS, FastAPI, and Ollama.

## Architecture

User Query -> FastAPI -> Router Agent -> DIRECT or RETRIEVE -> RAG -> FAISS -> LLM -> Response

## Features

- LangGraph agentic routing
- FAISS semantic retrieval
- Local Ollama LLM support
- Session-scoped conversational memory
- TXT/MD/PDF ingestion
- FastAPI REST API and Swagger
- Source-aware retrieval results
- Lightweight keyword evaluation endpoint
- Pytest tests
- Docker support

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
ollama pull llama3.2:3b
ollama serve
uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

## API

- `GET /health`
- `POST /documents`
- `POST /search`
- `POST /chat`
- `POST /evaluate`

Example chat body:

```json
{"query":"What encryption standard is required?","session_id":"demo"}
```

## Structure

```text
enterprise-agentic-rag/
├── app/
│   ├── agents/
│   ├── core/
│   ├── rag/
│   ├── services/
│   └── tools/
├── data/
├── tests/
├── Dockerfile
├── requirements.txt
└── main.py
```

## Production extensions

For a production deployment, add authentication, persistent vector storage, external session storage, tracing, rate limiting, and stronger automated RAG evaluation.
