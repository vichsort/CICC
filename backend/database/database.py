"""
Módulo de abstração e conexão com o banco de dados.

Este script suporta tanto SQLite (padrão e recomendado para totens/ambientes locais)
quanto PostgreSQL. Ele gerencia as conexões, simplifica a execução de queries com
parâmetros seguros e exporta uma instância única `db`.
"""

import os
import sqlite3
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Database:
    """
    Handler agnóstico para gerenciar operações com SQLite ou PostgreSQL.
    """

    def __init__(self):
        self.db_type = os.environ.get('DB_TYPE', 'sqlite').strip().lower()
        
        # Caminho padrão para o arquivo SQLite no diretório backend
        backend_dir = Path(__file__).resolve().parent.parent
        sqlite_filename = os.environ.get('SQLITE_FILE', 'database.sqlite3')
        self.sqlite_path = str(backend_dir / sqlite_filename)

        # Parâmetros para PostgreSQL
        self.db_params = {
            'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432')
        }

        # Inicializa o banco SQLite na primeira execução se for o caso
        if self.db_type == 'sqlite':
            self._init_sqlite()

    def _init_sqlite(self):
        """
        Inicializa o arquivo SQLite com WAL mode e garante que a tabela exista.
        """
        with sqlite3.connect(self.sqlite_path) as conn:
            # Habilita WAL (Write-Ahead Logging) para resiliência contra quedas de energia
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout = 5000;")
            
            # Garante que a tabela de emissões exista
            conn.execute("""
                CREATE TABLE IF NOT EXISTS emission_records (
                    id_record INTEGER PRIMARY KEY AUTOINCREMENT,
                    emission_amount REAL NOT NULL,
                    distance REAL NOT NULL,
                    people_amount INTEGER,
                    vehicle TEXT NOT NULL,
                    fuel TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

    def query(self, query_str: str, args: tuple = None):
        """
        Executa uma query SQL no banco configurado (SQLite ou PostgreSQL).

        Args:
            query_str (str): Query SQL com placeholders '%s'.
            args (tuple, optional): Tupla de argumentos para a query.

        Returns:
            list[dict]: Para consultas SELECT, lista de dicionários com as linhas.
            int: Para INSERT/UPDATE/DELETE, o número de linhas afetadas.
        """
        args = args or ()

        if self.db_type == 'sqlite':
            return self._query_sqlite(query_str, args)
        else:
            return self._query_postgres(query_str, args)

    def _query_sqlite(self, query_str: str, args: tuple):
        """Executa a query usando SQLite."""
        # Remove eventuais prefixos de schema 'public.' para compatibilidade com SQLite
        cleaned_query = query_str.replace('public.', '').replace('PUBLIC.', '')
        
        # Converte placeholders '%s' do PostgreSQL para '?' do SQLite
        adapted_query = cleaned_query.replace('%s', '?')

        with sqlite3.connect(self.sqlite_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(adapted_query, args)

            stripped = adapted_query.strip().lower()
            if stripped.startswith('select'):
                rows = cursor.fetchall()
                # Converte cada linha sqlite3.Row em dicionário comum
                return [dict(row) for row in rows]
            else:
                conn.commit()
                return cursor.rowcount

    def _query_postgres(self, query_str: str, args: tuple):
        """Executa a query usando PostgreSQL via psycopg."""
        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(**self.db_params, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_str, args)

                stripped = query_str.strip().lower()
                if stripped.startswith('select'):
                    return cursor.fetchall()
                else:
                    return cursor.rowcount


# Instância única da classe Database
db = Database()