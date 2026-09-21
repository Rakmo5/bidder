import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import tenders, bidders, evaluate, reports, iam, ocr, gem, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Bid Compliance Verification & Anti-Cartelization Engine for Ministry of Petroleum and Natural Gas (MoPNG) & GeM Integration",
    version="2.0.0"
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
app.include_router(tenders.router, prefix=f"{settings.API_V1_STR}/tenders", tags=["Tenders & Thresholds"])
app.include_router(bidders.router, prefix=f"{settings.API_V1_STR}/bidders", tags=["Bidders & Dossiers"])
app.include_router(evaluate.router, prefix=f"{settings.API_V1_STR}/evaluate", tags=["Evaluation & Forensics"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["Reports & Statutory Notices"])
app.include_router(iam.router, prefix=f"{settings.API_V1_STR}/iam", tags=["IAM & Audit Logging"])
app.include_router(ocr.router, prefix=f"{settings.API_V1_STR}/ocr", tags=["OCR Pipeline & Evidence"])
app.include_router(gem.router, prefix=f"{settings.API_V1_STR}/gem", tags=["GeM & OCDS Integration"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI & RAG Pipeline"])

@app.get("/")
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "version": "2.0.0",
        "supported_ministries": ["Ministry of Petroleum & Natural Gas (MoPNG)", "Ministry of Road Transport & Highways (MoRTH)"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "groq_configured": bool(settings.GROQ_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "ocr_pipeline": "PyMuPDF / Active",
        "iam_security": "Role-Based Access Control / Active",
        "gem_sync": "GeM 3.0 / OCDS 1.1.5 Ready"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)

