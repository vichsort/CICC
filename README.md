<div align="center">

<img src="frontend/src/assets/ita.png" alt="Consórcio Itá Logo" height="75" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="frontend/src/assets/ifc.png" alt="IFC Logo" height="75" />

# CICC — Calculadora de Impacto de Carbono

**Totem interativo e inteligente para conscientização ecológica e cálculo de pegada de carbono.**  
Calculando emissões de viagens e transformando dados em ações de reflorestamento.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org)
[![Vite](https://img.shields.io/badge/Vite-7.0-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Waitress](https://img.shields.io/badge/WSGI-Waitress-FF6F00?style=flat-square)](https://docs.pylonsproject.org/projects/waitress)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
</div>

---

<div align="center">
  <video src="assets/cicc_record.mp4" width="90%" autoplay loop muted playsinline></video>
</div>

---

## Sobre o projeto

O **CICC (Calculadora de Impacto de Carbono)** é um sistema interativo desenvolvido para rodar em **totens físicos de autoatendimento** e quiosques informativos. Fruto da parceria entre o **Consórcio Itá** e o **Instituto Federal Catarinense (IFC - Campus Concórdia)**, o projeto busca sensibilizar a população sobre o impacto ambiental de seus deslocamentos diários.

Ao registrar uma viagem, a aplicação calcula instantaneamente a quantidade de dióxido de carbono ($CO_2$) emitida com base em fatores de emissão oficiais por tipo de veículo, combustível e quantidade de passageiros. O sistema consolida esses dados em um painel em tempo real e calcula a estimativa de **árvores necessárias para compensar as emissões** (considerando a métrica de 7 árvores por tonelada de $CO_2$).

Projetado para operar com **estabilidade total e consumo mínimo de recursos**, o sistema dispensa Docker e serviços pesados no hardware do totem, iniciando em menos de 3 segundos após uma queda de energia.

### Funcionalidades

- **Cálculo Preciso de Emissões:** Lógica parametrizada por categoria (carro, moto, ônibus), tipo de motor (standard, flex, diesel) e ocupação do veículo.
- **Dashboard Dinâmico em Tempo Real:** Visualização gráfica com métricas de $CO_2$ acumulado, quilometragem total e gráficos interativos com D3.js.
- **Compensação Ecológica:** Estimativa automática de árvores necessárias para neutralização do carbono.
- **Modo Quiosque / Totem Nativo:** Execução em tela cheia via Microsoft Edge ou Google Chrome sem barras de navegação ou atalhos indesejados.
- **Timer de Inatividade Inteligente:** Reset automático do formulário após 60 segundos de inatividade, retornando à tela inicial.
- **Banco de Dados Híbrido:** Suporte automático para **SQLite** nativo (com modo WAL contra quedas de energia) ou **PostgreSQL**.
- **Exportação Tripla de Dados:**
  - **Easter Egg na UI:** 5 toques rápidos na logo do Consórcio Itá no rodapé abrem um modal com PIN para download direto do CSV.
  - **Via Script CLI:** `python backend/export_emissions.py` gera o arquivo formatado para Excel em 1 clique.
  - **Via Rede:** Endpoint HTTP protegido por PIN para download remoto por outros dispositivos da rede local.

---

## Arquitetura

O projeto adota uma arquitetura em camadas desacopladas (**Controller -> Service -> Database Adapter**), isolando as regras de negócio e persistência de dados das rotas HTTP e do frontend.

```
CICC/
├── assets/                  # Mídias e vídeos de demonstração
│   └── cicc_record.mp4
├── backend/                 # API RESTful Flask & Serviços
│   ├── database/            # Conector agnóstico (SQLite WAL + PostgreSQL)
│   ├── services/            # Regras de negócio, cálculos e queries (EmissionService)
│   ├── schemas/             # Schemas Pydantic para validação estrita
│   ├── routes/              # Controllers RESTful (Flask Blueprints)
│   ├── utils/               # Calculadora matemática de fatores de CO₂
│   ├── export_emissions.py  # Script CLI autônomo para exportação CSV
│   └── server.py            # Servidor WSGI de produção (Waitress)
├── frontend/                # Interface SPA em Vue 3 + Vite
│   ├── src/
│   │   ├── components/      # Telas (Dashboard, Formulário, Gráficos D3, Footer)
│   │   ├── services/        # Cliente HTTP centralizado (API Client)
│   │   ├── constants/       # Opções e categorias de emissão
│   │   └── composables/     # useInactivityTimeout para totens
│   └── dist/                # Build estático servido pelo Flask
├── start.bat                # 1-Clique p/ Totem no Windows (Waitress + Edge Kiosk)
├── dev.bat                  # Modo desenvolvimento local (Flask + Vite)
├── start.sh                 # 1-Clique p/ Linux
└── .env.example             # Modelo de configuração de ambiente
```

---

## Stack Tecnológica

| Camada | Tecnologia | Descrição |
|---|---|---|
| **Frontend Framework** | Vue.js 3 (Composition API) | Interface reativa e componentes modulares |
| **Frontend Build Tool** | Vite 7 | Bundler ultrarrápido com hot-reload |
| **Gráficos & Visualização** | D3.js v7 | Renderização de gráficos de pizza e barras |
| **Estilização** | Bootstrap 5 + CSS Scoped | Design responsivo adaptado para toque |
| **Backend Framework** | Python 3.12 + Flask 3.1 | API RESTful e servidor de arquivos SPA |
| **Servidor de Produção** | Waitress 3.0 | WSGI multithreaded leve para Windows/Linux |
| **Validação de Tipos** | Pydantic v2 + Pyright | Validação estrita de contratos de dados |
| **Banco de Dados (Padrão)** | SQLite 3 (Modo WAL) | Banco local embutido sem necessidade de servidor |
| **Banco de Dados (Opcional)**| PostgreSQL 16 via Psycopg 3 | Conexão para instâncias corporativas externas |

---

## Como Executar

### Pré-requisitos
- [Python 3.10+](https://python.org)
- [Node.js 18+](https://nodejs.org) *(Necessário apenas para compilar o frontend)*

---

### Instalação

#### 1. Clone o repositório
```bash
git clone https://github.com/vichsort/CICC.git
cd CICC
```

#### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv .venv

# No Windows:
.venv\Scripts\activate

# No Linux/Mac:
source .venv/bin/activate
```

#### 3. Instale as dependências
```bash
pip install -r backend/requirements.txt
```

#### 4. Compile o frontend para produção
```bash
npm --prefix frontend install
npm --prefix frontend run build
```

---

### Executando a Aplicação

#### 1. Modo Totem / Produção (Recomendado para Quiosques)

* **No Windows:** Dê dois cliques no arquivo **`start.bat`**.  
  *O script ativa o ambiente virtual, inicia o backend com Waitress em segundo plano e abre o Microsoft Edge automaticamente em tela cheia (`--kiosk`).*
* **No Linux:** Execute:
  ```bash
  ./start.sh
  ```

#### 2. Modo Desenvolvimento (com Hot-Reload)

* **No Windows:** Dê dois cliques no arquivo **`dev.bat`**.
* **Manualmente (Linux/Mac/Windows):**
  ```bash
  # Terminal 1 - Backend:
  flask --app backend.app run --debug --port 5000

  # Terminal 2 - Frontend:
  npm --prefix frontend run dev
  ```

---

## Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

| Variável | Padrão | Descrição |
|---|---|---|
| `DB_TYPE` | `sqlite` | Tipo de banco de dados (`sqlite` ou `postgres`) |
| `SQLITE_FILE` | `database.sqlite3` | Nome do arquivo do banco SQLite local |
| `ADMIN_PIN` | `1234` | Senha de administração (para 5 cliques na logo e endpoint `/export`) |
| `PORT` | `5000` | Porta TCP de execução da aplicação web |
| `DB_HOST` | `localhost` | Host do PostgreSQL *(apenas se `DB_TYPE=postgres`)* |
| `DB_PORT` | `5432` | Porta do PostgreSQL *(apenas se `DB_TYPE=postgres`)* |
| `DB_NAME` | `emissions_db` | Nome do banco PostgreSQL |
| `DB_USER` | `postgres` | Usuário do banco PostgreSQL |
| `DB_PASSWORD` | `strong_password`| Senha do banco PostgreSQL |

---

## Exportação de Relatórios

O sistema oferece três formas práticas de extrair os registros coletados:

1. **Pela Interface do Totem (Easter Egg):**
   * Dê **5 toques rápidos na logo do Consórcio Itá** no rodapé da página.
   * Insira o PIN administrativo configurado no `.env` (padrão `1234`).
   * Clique no botão **"Baixar Relatório (CSV)"**.
2. **Via Script de Terminal:**
   ```bash
   python backend/export_emissions.py
   ```
   *Gera o arquivo `emissions_AAAA-MM-DD.csv` pronto para abrir no Excel com acentuação e separadores brasileiros.*
3. **Pela Rede Local via Navegador:**
   * Acesse `http://<IP-DO-TOTEM>:5000/api/emission/export?pin=1234` de qualquer celular ou computador na mesma rede.

---

## Endpoints da API REST

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/api/emission/` | Registra uma nova viagem e calcula a emissão de $CO_2$ |
| `GET` | `/api/emission/` | Retorna todos os registros cadastrados |
| `GET` | `/api/emission/co2/` | Retorna soma total de $CO_2$ e estimativa de árvores |
| `GET` | `/api/emission/km/` | Retorna a distância total percorrida |
| `GET` | `/api/emission/vehicles/` | Lista veículos utilizados |
| `GET` | `/api/emission/fuels/` | Lista combustíveis utilizados |
| `POST` | `/api/emission/verify-pin` | Valida o PIN administrativo informado |
| `GET` | `/api/emission/export` | Download do relatório CSV (`?pin=...` ou header `X-Admin-Pin`) |

---

## Realização e Equipe

* **Realização:** [Consórcio Itá](https://consorcioita.com.br) & [Instituto Federal Catarinense (IFC)](https://concordia.ifc.edu.br)
* **Desenvolvedores:**
  * [Gabriel Moura Jappe](https://github.com/jappejappe) ([@jappejappe](https://github.com/jappejappe))
  * [Gustavo Schwitzki Peretti](https://github.com/GustavoPeretti) ([@GustavoPeretti](https://github.com/GustavoPeretti))
  * [Vitor Marcelo Mignoni](https://github.com/vichsort) ([@vichsort](https://github.com/vichsort))
  * Heitor Scalco Neto

---

<div align="center">
  <sub>Promovendo a sustentabilidade através da tecnologia 🌱⚡ Consórcio Itá & IFC</sub>
</div>