@echo off
title CICC - Modo Desenvolvimento

cd /d "%~dp0"

echo ===================================================
echo Iniciando CICC em Modo Desenvolvimento...
echo ===================================================

:: Inicia o Backend Flask com auto-reload
start "CICC Backend (Dev)" cmd /k "if exist .venv\Scripts\activate.bat (call .venv\Scripts\activate.bat) else (call backend\.venv\Scripts\activate.bat 2>nul) && cd backend && flask run --debug"

:: Inicia o Frontend Vite com hot-reload
start "CICC Frontend (Vite)" cmd /k "cd frontend && npm run dev"

exit

