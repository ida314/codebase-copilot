# Cold-Start-Copilot

This project is a work in progress.  
Check out the frontend repo here: https://github.com/ida314/codebase-copilot-web

**Onboard to any codebase in seconds.** An AI-powered code assistant that indexes your repository and answers questions about it with sub-second latency.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

Note: All benchmark metrics are placeholders, project is still WIP

- **Lightning Fast** - Index 15k LOC in <30s, answer queries in <800ms p95
- **Smart Chunking** - Language-aware code splitting with AST parsing
- **Semantic Search** - BGE-M3 embeddings with Qdrant vector store
- **Git History** - Answers "why" questions using commit history
- **Observable** - Built-in metrics with Langfuse & OpenTelemetry
- **Streaming** - Real-time SSE responses for instant feedback

## Quick Start

### Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Index Your Repository

WIP

```bash
python cold_start_copilot.py --repo ~/your/project --git-history
# Output: Indexed 432 chunks in 28.3s
```

### Start the API

WIP

```bash
uvicorn cold_start_copilot:app --reload --port 8000
```

### Ask Questions

WIP

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I run tests?"}'
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  Your Repo  │────▶│   Chunker    │────▶│  BGE-M3    │
└─────────────┘     └──────────────┘     └────────────┘
                            │                    │
                            ▼                    ▼
                    ┌──────────────┐     ┌────────────┐
                    │   Qdrant     │◀────│ Embeddings │
                    └──────────────┘     └────────────┘
                            │
                            ▼
                    ┌──────────────┐     ┌────────────┐
                    │   FastAPI    │────▶│   Llama3   │
                    └──────────────┘     └────────────┘
```

## Performance

Note: All benchmark metrics are placeholders, project is still WIP

| Metric | Value |
|--------|-------|
| Indexing Speed | 15k LOC in 28s |
| Query Latency (p95) | <800ms |
| Embedding Dimension | 768 (BGE-M3) |
| Context Window | 200 tokens |
| Supported Languages | Python, JS, TS, Go, Rust, Java, C++ |

## Docker Deploy

WIP

```yaml
docker-compose up -d
```

Your code assistant is now running at `http://localhost:8000`

## API Endpoints

WIP

- `POST /index` - Index a repository
- `POST /chat` - Ask questions about code
- `GET /chat/stream` - Stream responses (SSE)
- `GET /health` - Service health check
- `GET /metrics` - Performance metrics

## Frontend

WIP

Check out the [web UI](./frontend) for a beautiful chat interface built with Vite + shadcn/ui.

## License

MIT
