@echo off
title GenoTrace - Starting UI
cd /d "%~dp0"
set PYTHONPATH=src

echo ========================================
echo           GENOTRACE UI LAUNCHER
echo ========================================
echo.
echo Starting Clinical Decision Support Platform...
echo.
echo Local URL: http://localhost:8501
echo.
echo To stop the app, press CTRL+C in this window
echo ========================================
echo.

"C:\Users\HP\AppData\Local\Programs\Python\Python310\python.exe" -m streamlit run app\Home.py

pause
