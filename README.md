
# Calculadora de Emissão de Carbono - Consórcio Itá

## 📝 Sumário

  * [Sobre o Projeto](https://www.google.com/search?q=%23-sobre-o-projeto)
  * [✨ Funcionalidades](https://www.google.com/search?q=%23-funcionalidades)
  * [🛠️ Tecnologias Utilizadas](https://www.google.com/search?q=%23%EF%B8%8F-tecnologias-utilizadas)
  * [🚀 Começando](https://www.google.com/search?q=%23-come%C3%A7ando)
      * [Pré-requisitos](https://www.google.com/search?q=%23pr%C3%A9-requisitos)
      * [Instalação](https://www.google.com/search?q=%23instala%C3%A7%C3%A3o)
      * [Configuração do Banco de Dados](https://www.google.com/search?q=%23configura%C3%A7%C3%A3o-do-banco-de-dados)
      * [Executando a Aplicação](https://www.google.com/search?q=%23executando-a-aplica%C3%A7%C3%A3o)
  * [🔌 Uso da API](https://www.google.com/search?q=%23-uso-da-api)

## 📖 Sobre o Projeto

Este projeto consiste em uma API RESTful desenvolvida para calcular e registrar a emissão de dióxido de carbono (CO₂) gerada a partir de viagens. A aplicação recebe dados como distância, tipo de veículo, combustível e número de passageiros, calcula a emissão correspondente e armazena o registro em um banco de dados para futuras análises.

## ✨ Funcionalidades

  - [x] **Cálculo de Emissão:** Lógica para calcular a emissão de CO₂ com base em diferentes parâmetros.
  - [x] **API para Registro:** Endpoint `POST` para receber os dados e criar um novo registro de emissão.
  - [x] **Persistência de Dados:** Integração com banco de dados PostgreSQL para armazenar os registros.
  - [x] **Estrutura Modular:** Uso de Blueprints do Flask para organizar as rotas de forma escalável.

## 🛠️ Tecnologias Utilizadas

  * **Backend:** Python 3, Flask
  * **Banco de Dados:** PostgreSQL
  * **Gerenciador de Pacotes:** PIP
  * **Ambiente Virtual:** venv

## 🚀 Começando

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

  * [Python 3.8+](https://www.python.org/downloads/)
  * [Git](https://git-scm.com/)
  * [PostgreSQL](https://www.postgresql.org/download/) (ou um container Docker com a imagem do Postgres)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/jappejappe/Emissao_de_Carbono_Consorcio.git
    ```

2.  **Acesse o diretório do backend:**

    ```bash
    cd Emissao_de_Carbono_Consorcio/backend
    ```

3.  **Crie e ative o ambiente virtual:**

      * No **Windows**:
        ```bash
        py -3 -m venv .venv
        .venv\Scripts\activate
        ```
      * No **Linux/Mac**:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

4.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuração do Banco de Dados

1.  **Crie um banco de dados** no PostgreSQL para a aplicação (ex: `emissions_db`).

2.  **Crie a tabela `emission_records`**. Execute o seguinte comando SQL no seu banco de dados:

    ```sql
    CREATE TABLE public.emission_records (
        id SERIAL PRIMARY KEY,
        person_name VARCHAR(255) NOT NULL,
        emission_amount NUMERIC(10, 4) NOT NULL,
        distance NUMERIC(10, 2) NOT NULL,
        people_amount INTEGER,
        vehicle VARCHAR(100),
        fuel VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    ```

3.  **Configure as variáveis de ambiente.** Crie um arquivo chamado `.env` na pasta `backend` e adicione as credenciais do seu banco de dados.

    ```ini
    # .env
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=emissions_db
    DB_USER=seu_usuario_postgres
    DB_PASSWORD=sua_senha_postgres
    ```

    > **Atenção:** O código da sua aplicação precisa ser ajustado para ler essas variáveis de ambiente (usando bibliotecas como `python-dotenv`).

### Executando a Aplicação

Com o ambiente virtual ativado, inicie o servidor Flask:

```bash
flask run
```

A API estará disponível em `http://127.0.0.1:5000`.

## 🔌 Uso da API

A API possui um endpoint principal para criar registros de emissão.

### Criar Registro de Emissão

Cria um novo registro de emissão com base nos dados da viagem.

  - **Endpoint:** `POST /api/emission/`

  - **Método:** `POST`

  - **Corpo da Requisição (JSON):**

    ```json
    {
        "person_name": "João da Silva",
        "distance": 150.5,
        "people_amount": 2,
        "vehicle": "car",
        "fuel": "gasoline",
        "vehicle_type": "standard"
    }
    ```

  - **Resposta de Sucesso (Código `201 Created`):**

    ```json
    {
        "ok": true,
        "message": "Registro de emissão criado para João da Silva. Emissão calculada: 35.82 kg CO₂."
    }
    ```

  <br>

  - **Endpoint:** `GET /api/emission/`

  - **Método:** `GET`

  - **Resposta de Sucesso (Código `200 OK`):**

    ```json
    [
      {
        "distance": "23.00",
        "emission_amount": "0.585",
        "fuel": "gasoline",
        "id_record": 4,
        "people_amount": 3,
        "person_name": "Gabriel",
        "vehicle": "car-standard"
      },
      {
        "distance": "11.00",
        "emission_amount": "0.198",
        "fuel": "gasoline",
        "id_record": 5,
        "people_amount": 2,
        "person_name": "Maria",
        "vehicle": "motorcycle-standard"
      }
    ]
    ```

  <br>

  - **Endpoint:** `GET /api/emission/co2/`

  - **Método:** `GET`

  - **Resposta de Sucesso (Código `200 OK`):**

    ```json
    {
      "records": [
        {
          "emission_amount": "0.585"
        },
        {
          "emission_amount": "0.198"
        }
      ],
      "total_co2": "0.783"
    }
    ```

  <br>

  - **Endpoint:** `GET /api/emission/vehicles/`

  - **Método:** `GET`

  - **Resposta de Sucesso (Código `200 OK`):**

    ```json
    [
      {
        "vehicle": "car-standard"
      },
      {
        "vehicle": "motorcycle-flex"
      }
    ]
    ```

  <br>

  - **Endpoint:** `GET /api/emission/fuels/`

  - **Método:** `GET`

  - **Resposta de Sucesso (Código `200 OK`):**

    ```json
    [
      {
        "fuel": "gasoline"
      },
      {
        "fuel": "diesel"
      }
    ]
    ```

  <br>

  - **Endpoint:** `GET /api/emission/km/`

  - **Método:** `GET`

  - **Resposta de Sucesso (Código `200 OK`):**

    ```json
    {
      "records": [
        {
          "distance": "23.00"
        },
        {
          "distance": "11.00"
        }
      ],
      "total_km": "34.00"
    }
    ```