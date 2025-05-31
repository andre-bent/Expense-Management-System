@echo off
start cmd /k "uvicorn backend.server:app --reload"
timeout /t 3 >nul  # Wait 3 seconds before launching Streamlit
start cmd /k "streamlit run frontend/main.py"