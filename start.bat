@echo off
title CICC - Calculadora de Emissoes de Carbono (Modo Totem)

:: Garante que o diretorio atual seja a raiz do projeto
cd /d "%~dp0"

:: Localiza e ativa o ambiente virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "backend\.venv\Scripts\activate.bat" (
    call backend\.venv\Scripts\activate.bat
) else (
    echo [AVISO] Ambiente virtual (.venv) nao encontrado. Executando com o Python global...
)

:: Inicia o servidor backend com Waitress em segundo plano (janela minimizada)
start "CICC Backend Server" /min python backend/server.py

:: Aguarda 2 segundos para o servidor subir
timeout /t 2 /nobreak >nul

:: Inicia o Microsoft Edge em Modo Quiosque Fullscreen
start msedge --kiosk http://localhost:5000 --edge-kiosk-type=fullscreen --no-first-run --disable-pinch --overscroll-history-navigation=0

exit