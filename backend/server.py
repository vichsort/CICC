"""
Servidor WSGI de produção usando Waitress.

Ultraleve, multithreaded, nativo em Python e ideal para Windows/Totens e servidores.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
root_dir: Path = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app import app
import waitress


def run_server() -> None:
    """Inicia o servidor web na porta configurada com Waitress."""
    port: int = int(os.environ.get('PORT', 5000))
    host: str = os.environ.get('HOST', '0.0.0.0')

    print("=" * 50)
    print("🚀 Servidor CICC Iniciado com Sucesso!")
    print(f"📍 Endereço local: http://localhost:{port}")
    print(f"📡 Endereço de rede: http://{host}:{port}")
    print("=" * 50)

    waitress.serve(app, host=host, port=port, threads=4)


if __name__ == '__main__':
    run_server()

