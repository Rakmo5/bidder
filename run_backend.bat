@echo off
echo ================================================================
echo Starting MoPNG AI Bid Compliance Verification Backend (FastAPI)
echo ================================================================
cd /d "%~dp0"
call .\venv\Scripts\activate
uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
pause
