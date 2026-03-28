# Finn — FinTech AI Assistant API

A production-ready conversational AI API built with FastAPI and Claude (Anthropic). 
Designed for financial professionals in the GCC and European markets.

## Features

- Claude Sonnet powered chat with full conversation memory
- Streaming responses via Server-Sent Events (SSE)
- Input validation and sanitization
- Sliding window rate limiting (10 req/min per IP)
- Structured logging with daily rotating log files
- Fully containerized with Docker

## Tech Stack

- **LLM:** Claude Sonnet (Anthropic)
- **Backend:** FastAPI + Python 3.12
- **Containerization:** Docker + Docker Compose
- **Validation:** Pydantic v2

## Quick Start

### Without Docker
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### With Docker
```bash
docker compose up --build
```

## Environment Variables

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_key_here
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Standard chat response |
| POST | `/chat/stream` | Streaming chat response (SSE) |

## Example Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is compound interest?", "history": []}'
```

## Example Response
```json
{
  "response": "Compound interest is...",
  "history": [
    {"role": "user", "content": "What is compound interest?"},
    {"role": "assistant", "content": "Compound interest is..."}
  ]
}
```

## Project Structure
```
app/
├── api/routes.py          # REST endpoints
├── services/llm_service.py # Claude API integration
├── core/
│   ├── config.py          # Configuration and constants
│   └── logging_config.py  # Structured logging setup
├── middleware/
│   └── rate_limiter.py    # Rate limiting middleware
└── main.py                # FastAPI application entry point
```