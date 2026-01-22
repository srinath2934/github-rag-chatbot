@echo off
REM GitHub RAG Chatbot - Startup Script for Windows

echo ============================================
echo   GitHub RAG Chatbot - Starting...
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "rag_env\" (
    echo ERROR: Virtual environment 'rag_env' not found!
    echo Please run: python -m venv rag_env
    echo Then run: .\rag_env\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with:
    echo   GROQ_API_KEY=your_key_here
    echo   GITHUB_TOKEN=your_token_here
    echo.
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo Please edit .env and add your API keys!
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call .\rag_env\Scripts\activate.bat
echo.

echo [2/3] Checking dependencies...
pip list | findstr streamlit >nul 2>&1
if errorlevel 1 (
    echo WARNING: Dependencies not installed!
    echo Installing requirements...
    pip install -r requirements.txt
    echo.
)

echo [3/3] Starting Streamlit app...
echo.
echo ============================================
echo   App will open at http://localhost:8501
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

streamlit run app.py

pause
