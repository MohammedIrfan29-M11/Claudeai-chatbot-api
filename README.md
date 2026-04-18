# Finn — FinTech AI Assistant API

> A production-grade conversational AI API for financial professionals in the GCC and European markets. Powered by Claude Sonnet with streaming responses, rate limiting, and full Docker deployment.

🔴 **Live API:** https://claudeai-chatbot-api-production.up.railway.app  
📖 **Interactive Docs:** https://claudeai-chatbot-api-production.up.railway.app/docs  
💻 **GitHub:** https://github.com/MohammedIrfan29-M11/Claudeai-chatbot-api

---

## What it does

A FinTech-specialised AI assistant that handles financial queries with conversation memory, streaming responses, and production-grade reliability.

```bash
# Standard chat
curl -X POST https://claudeai-chatbot-api-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain compound interest with a practical example", "history": []}'

# Streaming chat (tokens appear word by word)
curl -N -X POST https://claudeai-chatbot-api-production.up.railway.app/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "What is dollar cost averaging?", "history": []}'
```

---

## Features

- **Claude Sonnet 4.5** — domain-specific system prompt for GCC and EU financial markets
- **Streaming responses** — Server-Sent Events (SSE) for real-time token delivery
- **Stateless conversation memory** — client-managed history, server stays stateless
- **Rate limiting** — sliding window algorithm, 10 requests/minute per IP
- **Input validation** — Pydantic v2 validators, sanitization, length limits
- **Structured logging** — timestamped logs with module names, daily log rotation
- **Docker** — containerized with health checks and volume persistence
- **CORS** — cross-origin support for frontend integration

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Standard chat response |
| POST | `/chat/stream` | Streaming response via SSE |

Full interactive documentation at `/docs`.

---

## Architecture decisions

**Why stateless history?**
The client sends full conversation history with every request and receives the updated history back. This makes the API horizontally scalable — any server instance handles any request without shared state. Server-side history would require sticky sessions or a shared cache, adding operational complexity.

**Why sliding window rate limiting?**
Sliding window counts requests in a rolling 60-second window rather than resetting at fixed intervals. This prevents burst attacks at window boundaries (e.g., 10 requests at :59 and 10 at :01 of the next minute). In production this would use Redis for distributed enforcement across multiple instances.

**Why SSE over WebSockets for streaming?**
Server-Sent Events are unidirectional (server → client), which is all we need for streaming LLM responses. WebSockets add bidirectional complexity that isn't required here. SSE also works over standard HTTP and doesn't require protocol upgrades.

---

## Tech Stack

- **LLM:** Claude Sonnet 4.5 (Anthropic)
- **Backend:** FastAPI + Python 3.12
- **Streaming:** Server-Sent Events (SSE)
- **Validation:** Pydantic v2
- **Containerization:** Docker + Docker Compose
- **Deployment:** Railway

---

## Quick Start

### Local development

```bash
git clone https://github.com/MohammedIrfan29-M11/Claudeai-chatbot-api
cd Claudeai-chatbot-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

Run:
```bash
uvicorn app.main:app --reload
```

### Docker

```bash
docker compose up --build
```

---

## Project Structure

```
app/
├── api/routes.py              # /chat and /chat/stream endpoints
├── services/llm_service.py    # Claude API + streaming generator
├── middleware/rate_limiter.py # Sliding window rate limiting
├── core/
│   ├── config.py              # API key, validation constants
│   └── logging_config.py      # Structured logging setup
└── main.py                    # FastAPI app + CORS + middleware
```

---

## System Prompt Design

Finn is configured as a FinTech specialist for GCC and European markets with explicit hard boundaries:

- Never recommends specific stocks, funds, or investment products
- Never gives tax advice for specific situations  
- Always recommends a licensed financial advisor for personal decisions
- Refuses illegal financial activity requests clearly

Response format enforced in the system prompt: markdown, bullet points, and every complex answer ends with "Bottom line:" summary.

---


**Related project:** [EnergyRAG — Energy Policy Document Intelligence](https://github.com/MohammedIrfan29-M11/energy-rag-api)
