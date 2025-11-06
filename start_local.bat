@echo off
echo ========================================
echo Starting Streamlit App Locally
echo ========================================
echo.
echo Make sure you're in the project directory!
echo.
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Starting Streamlit...
echo Browser will open automatically at http://localhost:8501
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8501
python -m streamlit run app_streamlit.py
pause

