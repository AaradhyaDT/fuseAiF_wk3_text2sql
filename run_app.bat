@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo Launching Fuse AI Text-to-SQL app...
echo.

if exist ".venv\Scripts\activate.bat" (
    set PYTHON_ACTIVATE=.venv\Scripts\activate.bat
) else (
    set PYTHON_ACTIVATE=
)

if not defined PYTHON_ACTIVATE (
    echo WARNING: Virtual environment not found at .venv\Scripts\activate.bat
    echo Make sure Python 3.11+ is installed and dependencies are installed.
    echo.
) else (
    echo Virtual environment found.
)

if not exist ".env" (
    echo WARNING: .env file not found. Create .env with DB and API credentials if required.
    echo.
)

set BACKEND_CMD=python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
set STREAMLIT_CMD=python -m streamlit run streamlit_app.py

if defined PYTHON_ACTIVATE (
    set BACKEND_CMD=call %PYTHON_ACTIVATE% ^&^& %BACKEND_CMD%
    set STREAMLIT_CMD=call %PYTHON_ACTIVATE% ^&^& %STREAMLIT_CMD%
)

start "Fuse AI Backend" cmd /k "cd /d "%~dp0" && %BACKEND_CMD%"
timeout /t 2 >nul
start "Fuse AI Streamlit" cmd /k "cd /d "%~dp0" && %STREAMLIT_CMD%"
timeout /t 2 >nul
start "" "http://localhost:8501"
echo.
echo Backend on http://localhost:8000
echo Streamlit UI on http://localhost:8501
echo.
pause
