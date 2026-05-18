@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo Launching Fuse AI Text-to-SQL app with Docker Compose...
echo.

rem Ensure Docker is installed and the daemon is available
where docker >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH.
    echo Install Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker daemon does not appear to be running.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

rem Create a default .env file if missing
if not exist ".env" (
    echo Creating default .env file...
    >".env" echo # Docker Compose environment file for Fuse AI Text-to-SQL
    >>".env" echo DB_HOST=db
    >>".env" echo DB_PORT=5432
    >>".env" echo DB_NAME=classicmodels
    >>".env" echo DB_USER=postgres
    >>".env" echo DB_PASSWORD=password
    >>".env" echo GROQ_API_KEY=
    echo.
    echo NOTE: A .env file was created with default database settings.
    echo You must add your GROQ_API_KEY to .env before using the agent endpoints.
    echo.
)

rem Validate that GROQ_API_KEY is populated
for /f "usebackq tokens=1* delims==" %%A in (".env") do (
    if /i "%%A"=="GROQ_API_KEY" set GROQ_API_KEY=%%B
)

if "%GROQ_API_KEY%"=="" (
    echo ERROR: GROQ_API_KEY is not set in .env.
    echo Open .env, add your Groq API key as GROQ_API_KEY=your_key_here, then rerun this script.
    echo.
    start "Edit .env" notepad ".env"
    pause
    exit /b 1
)

rem Start Docker Compose in a new terminal and open the Streamlit UI
start "Fuse AI Docker" cmd /k "cd /d "%~dp0" && docker compose up --build"

echo Waiting for services to start...
timeout /t 10 >nul
start "" "http://localhost:8501"

echo.
echo Backend on http://localhost:8000
echo Streamlit UI on http://localhost:8501
echo.
echo If the browser does not load, wait a moment and refresh.
echo.
exit /b 0
