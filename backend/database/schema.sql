-- ==========================================================
-- Schema de Banco de Dados - Calculadora de Emissões (CICC)
-- ==========================================================

-- 1. Definição para PostgreSQL:
-- CREATE TABLE IF NOT EXISTS public.emission_records (
--     id_record SERIAL PRIMARY KEY,
--     emission_amount NUMERIC(10, 4) NOT NULL,
--     distance NUMERIC(10, 2) NOT NULL,
--     people_amount INT,
--     vehicle VARCHAR(100) NOT NULL,
--     fuel VARCHAR(100) NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );

-- 2. Definição para SQLite (criada automaticamente pelo backend):
CREATE TABLE IF NOT EXISTS emission_records (
    id_record INTEGER PRIMARY KEY AUTOINCREMENT,
    emission_amount REAL NOT NULL,
    distance REAL NOT NULL,
    people_amount INTEGER,
    vehicle TEXT NOT NULL,
    fuel TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);