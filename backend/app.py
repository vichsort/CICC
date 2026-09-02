"""
Aplicação principal Flask - Calculadora de Emissão de Carbono (CICC).

Configurada para servir a API RESTful e, em produção, servir o build SPA do frontend (Vue 3).
"""

from __future__ import annotations

import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.routes.api import api

# Localização da pasta dist gerada pelo build do Vue
FRONTEND_DIST: Path = Path(__file__).resolve().parent.parent / "frontend" / "dist"

app: Flask = Flask(
    __name__,
    static_folder=str(FRONTEND_DIST) if FRONTEND_DIST.exists() else None,
    static_url_path=''
)

# Habilita CORS para permitir requisições durante o desenvolvimento com Vite
CORS(app)

# Registra as rotas da API
app.register_blueprint(api, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path: str):
    """
    Serve o aplicativo frontend SPA (Vue).
    Qualquer rota não pertencente à API é direcionada para o index.html,
    garantindo compatibilidade com o HTML5 History Mode do Vue Router.
    """
    if FRONTEND_DIST.exists():
        target_file = FRONTEND_DIST / path
        if path and target_file.exists() and target_file.is_file():
            return send_from_directory(str(FRONTEND_DIST), path)
        return send_from_directory(str(FRONTEND_DIST), 'index.html')

    # Mensagem de desenvolvimento quando frontend/dist ainda não foi compilado
    return jsonify({
        'status': 'online',
        'message': 'API Flask CICC ativa. Para acessar o frontend, execute "npm run dev" ou gere o build com "npm run build".',
        'api_docs': '/api/emission/'
    }), 200


if __name__ == '__main__':
    # Permite rodar diretamente com python backend/app.py
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
