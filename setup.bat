@echo off
echo.
echo ========================================
echo   News Research Tool - Setup (Windows)
echo ========================================
echo.
echo [1/5] Checking Python...
python --version
if errorlevel 1 ( echo ERROR: Python not found. & pause & exit /b )
echo [2/5] Creating venv...
python -m venv venv
echo [3/5] Activating venv...
call venv\Scripts\activate
echo [4/5] Installing packages...
pip install --upgrade pip -q
pip install -r requirements.txt
echo [5/5] Done. .env already has your API keys.
echo.
echo ========================================
echo   Setup Complete!
echo   Run: streamlit run app.py
echo ========================================
pause
