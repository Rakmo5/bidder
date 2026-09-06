import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import tenders, bidders, evaluate, reports

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Bid Compliance Verification System for Ministry of Petroleum and Natural Gas & Public Works Tenders",
    version="1.0.0"
)

# Allow Cross-Origin Requests from Vite/React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(tenders.router, prefix=f"{settings.API_V1_STR}/tenders", tags=["Tenders"])
app.include_router(bidders.router, prefix=f"{settings.API_V1_STR}/bidders", tags=["Bidders"])
app.include_router(evaluate.router, prefix=f"{settings.API_V1_STR}/evaluate", tags=["Evaluation & Forensics"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["Reports & Export"])

@app.get("/")
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "groq_configured": bool(settings.GROQ_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
