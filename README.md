# Calculadora de Emissão de Carbono - Consórcio Itá (CICC)

Sistema interativo para totens de autoatendimento e painéis informativos para cálculo, registro e visualização de emissões de dióxido de carbono (CO₂) geradas a partir de viagens.

---

## 📝 Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Executar](#-como-executar)
  - [1. Modo Totem / Produção (Recomendado para Quiosques)](#1-modo-totem--produção-recomendado-para-quiosques)
  - [2. Modo Desenvolvimento](#2-modo-desenvolvimento)
- [Configuração do Banco de Dados](#-configuração-do-banco-de-dados)
  - [SQLite (Padrão, Sem Servidor)](#sqlite-padrão-sem-servidor)
  - [PostgreSQL (Opcional)](#postgresql-opcional)
- [Exportação de Dados](#-exportação-de-dados)
- [Endpoints da API REST](#-endpoints-da-api-rest)

---

## 📖 Visão Geral

Este projeto foi otimizado para rodar de forma ultraleve e resiliente em **totens de autoatendimento físicos** (mesmo com hardware modesto, como mini-PCs com 2GB/4GB de RAM rodando Windows ou Linux).

O backend em **Flask** serve diretamente a aplicação SPA compilada em **Vue 3**, e o servidor WSGI de produção **Waitress** gerencia as requisições de forma multithreaded e estável, **dispensando o uso de Docker ou Node.js na máquina final**.

---

## ✨ Funcionalidades Principais

- **Cálculo Preciso de CO₂:** Baseado em fatores de emissão oficiais por veículo (carro, moto, ônibus), tipo de combustível e número de passageiros.
- **Dashboard em Tempo Real:** Visualização gráfica com métricas de CO₂ acumulado, distância total percorrida e estimativa de árvores necessárias para compensação ecológica.
- **Banco de Dados Híbrido:** Suporte automático para **SQLite** nativo (com modo WAL contra quedas de energia) ou **PostgreSQL**.
- **UX Adaptada para Totem:**
  - Timer de inatividade de 60 segundos (auto-reset se o usuário abandonar a tela).
  - Bloqueio de seleções indesejadas de texto para telas sensíveis ao toque.
  - Modo Quiosque nativo em tela cheia com Microsoft Edge ou Google Chrome.
- **Exportação Tripla de Dados:**
  - **Na tela:** 5 toques rápidos na logo do Consórcio Itá abrem o modal com senha/PIN para download direto do CSV.
  - **Via Script CLI:** `python backend/export_emissions.py` gera a planilha em 1 clique na pasta Documentos.
  - **Via Rede:** Endpoint HTTP protegido por PIN para download remoto via navegador.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend:** Vue 3, Vite, Vue Router (HTML5 History Mode), Bootstrap 5, D3.js.
- **Backend:** Python 3.10+, Flask, Waitress (WSGI de Produção), Pydantic (validação estrita), SQLite3 / Psycopg.

---

## 🚀 Como Executar

### Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/) *(Apenas para compilar o frontend no ambiente de desenvolvimento)*

### Instalação Inicial
```bash
# 1. Clone o repositório
git clone https://github.com/vichsort/CICC.git
cd CICC

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv

# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências do backend
pip install -r backend/requirements.txt

# 4. Compile o frontend para produção
npm --prefix frontend install
npm --prefix frontend run build
```

---

### 1. Modo Totem / Produção (Recomendado para Quiosques)

#### No Windows:
Dê dois cliques no arquivo **`start.bat`**.
* Ele inicia o servidor com Waitress e abre o Microsoft Edge em tela cheia no modo quiosque (`--kiosk http://localhost:5000`).

#### No Linux:
Execute o script:
```bash
./start.sh
```

---

### 2. Modo Desenvolvimento

Para trabalhar no código com hot-reload no Vue e auto-reload no Flask:

#### No Windows:
Dê dois cliques no arquivo **`dev.bat`**.

#### Manualmente:
```bash
# Terminal 1 - Backend:
flask --app backend.app run --debug --port 5000

# Terminal 2 - Frontend:
npm --prefix frontend run dev
```

---

## 🗄️ Configuração do Banco de Dados

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

### SQLite (Padrão, Sem Servidor)
Configuração padrão recomendada para totens:
```ini
DB_TYPE=sqlite
SQLITE_FILE=database.sqlite3
```
*Não requer instalação de nenhum serviço. O arquivo é criado e gerenciado automaticamente na pasta `backend/`.*

### PostgreSQL (Opcional)
Se desejar conectar a uma instância externa do PostgreSQL:
```ini
DB_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=emissions_db
DB_USER=postgres
DB_PASSWORD=sua_senha
```

---

## 📊 Exportação de Dados

1. **Na Interface do Totem (Easter Egg):** Dê 5 toques rápidos na logo do *Consórcio Itá* no rodapé. Digite o PIN configurado (`ADMIN_PIN`, padrão `1234`) e clique em **"Baixar Relatório (CSV)"**.
2. **Via Script no Terminal:**
   ```bash
   python backend/export_emissions.py
   ```
   *Gera o arquivo `emissions_AAAA-MM-DD.csv` pronto para abrir no Excel com acentuação UTF-8.*
3. **Via Navegador pela Rede:**
   Acesse: `http://<IP-DO-TOTEM>:5000/api/emission/export?pin=1234`

---

## 🔌 Endpoints da API REST

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/emission/` | Registra uma nova emissão de CO₂ |
| `GET` | `/api/emission/` | Lista todos os registros de emissão |
| `GET` | `/api/emission/co2/` | Retorna total de CO₂ emitido e árvores necessárias |
| `GET` | `/api/emission/km/` | Retorna total de quilômetros registrados |
| `GET` | `/api/emission/vehicles/` | Lista veículos registrados |
| `GET` | `/api/emission/fuels/` | Lista combustíveis registrados |
| `POST` | `/api/emission/verify-pin` | Valida o PIN de administração |
| `GET` | `/api/emission/export` | Download do relatório CSV (requer `?pin=...`) |

---

## 👥 Realização e Desenvolvedores

* **Realização:** Consórcio Itá & Instituto Federal Catarinense (IFC)
* **Desenvolvedores:** Gabriel Moura Jappe, Gustavo Schwitzki Peretti, Vitor Marcelo Mignoni, Heitor Scalco Neto