import logging
from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging
from app.middleware.rate_limiter import rate_limit_middleware

setup_logging()
logger = logging.getLogger('app.main')

app = FastAPI(title = "Finn - Fintech Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limit_middleware)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Finn AI Assistant is running", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    logger.info("="*50)
    logger.info("Finn FinTech Assistant starting up")
    logger.info(f"Model: claude-sonnet-4-5")
    logger.info("="*50)