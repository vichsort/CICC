#!/usr/bin/env bash
# ==============================================================================
# Script de Execução CICC para Linux / Totens
# ==============================================================================

cd "$(dirname "$0")"

# Ativa o ambiente virtual se existir
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "backend/.venv/bin/activate" ]; then
    source backend/.venv/bin/activate
fi

# Inicia o servidor WSGI com Waitress
python3 backend/server.py &
SERVER_PID=$!

# Aguarda 2 segundos para o servidor inicializar
sleep 2

# Abre o navegador em tela cheia / quiosque
if command -v chromium-browser &> /dev/null; then
    chromium-browser --kiosk http://localhost:5000 &
elif command -v google-chrome &> /dev/null; then
    google-chrome --kiosk http://localhost:5000 &
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &
fi

# Aguarda o processo do servidor
wait $SERVER_PID

