"""
Módulo de abstração e conexão com o banco de dados.

Suporta SQLite (padrão com WAL e auto-criação) e PostgreSQL.
Completamente tipado para compatibilidade com linters estritos (Pylance/Pyright/Mypy).
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

try:
    from dotenv import load_dotenv
    _root_env: Path = Path(__file__).resolve().parent.parent.parent / '.env'
    _backend_env: Path = Path(__file__).resolve().parent.parent / '.env'
    if _root_env.exists():
        load_dotenv(dotenv_path=_root_env)
    elif _backend_env.exists():
        load_dotenv(dotenv_path=_backend_env)
    else:
        load_dotenv()
except ImportError:
    pass


class Database:
    """
    Handler agnóstico para gerenciar operações com SQLite ou PostgreSQL.
    """

    def __init__(self) -> None:
        self.db_type: str = os.environ.get('DB_TYPE', 'sqlite').strip().lower()
        
        # Caminho padrão para o arquivo SQLite no diretório backend
        backend_dir: Path = Path(__file__).resolve().parent.parent
        sqlite_filename: str = os.environ.get('SQLITE_FILE', 'database.sqlite3')
        self.sqlite_path: str = str(backend_dir / sqlite_filename)

        # Parâmetros para PostgreSQL
        self.db_params: Dict[str, str] = {
            'dbname': os.environ.get('DB_NAME', 'emissions_db'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', ''),
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432')
        }

        # Inicializa o banco SQLite na primeira execução se for o caso
        if self.db_type == 'sqlite':
            self._init_sqlite()

    def _init_sqlite(self) -> None:
        """
        Inicializa o arquivo SQLite com WAL mode e garante que a tabela exista.
        """
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout = 5000;")
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

    def query(self, query_str: str, args: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """
        Executa uma consulta SELECT e retorna a lista de registros como dicionários.
        """
        params: Tuple[Any, ...] = args if args is not None else ()

        if self.db_type == 'sqlite':
            return self._query_sqlite_select(query_str, params)
        return self._query_postgres_select(query_str, params)

    def execute(self, query_str: str, args: Optional[Tuple[Any, ...]] = None) -> int:
        """
        Executa uma instrução INSERT, UPDATE ou DELETE e retorna a quantidade de linhas afetadas.
        """
        params: Tuple[Any, ...] = args if args is not None else ()

        if self.db_type == 'sqlite':
            return self._query_sqlite_execute(query_str, params)
        return self._query_postgres_execute(query_str, params)

    def _clean_sqlite_query(self, query_str: str) -> str:
        """Remove referências a 'public.' e converte '%s' para '?'."""
        return query_str.replace('public.', '').replace('PUBLIC.', '').replace('%s', '?')

    def _query_sqlite_select(self, query_str: str, args: Tuple[Any, ...]) -> List[Dict[str, Any]]:
        adapted_query: str = self._clean_sqlite_query(query_str)
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(adapted_query, args)
            rows: List[sqlite3.Row] = cursor.fetchall()
            return [dict(row) for row in rows]

    def _query_sqlite_execute(self, query_str: str, args: Tuple[Any, ...]) -> int:
        adapted_query: str = self._clean_sqlite_query(query_str)
        with sqlite3.connect(self.sqlite_path) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(adapted_query, args)
            conn.commit()
            return cursor.rowcount

    def _get_postgres_conninfo(self) -> str:
        user = self.db_params.get('user', 'postgres')
        password = self.db_params.get('password', '')
        host = self.db_params.get('host', 'localhost')
        port = self.db_params.get('port', '5432')
        dbname = self.db_params.get('dbname', 'emissions_db')
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    def _query_postgres_select(self, query_str: str, args: Tuple[Any, ...]) -> List[Dict[str, Any]]:
        import psycopg
        from psycopg.rows import dict_row

        psycopg_module: Any = cast(Any, psycopg)
        with psycopg_module.connect(self._get_postgres_conninfo(), row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_str, args)
                rows: List[Any] = cursor.fetchall()
                return [dict(r) for r in rows]

    def _query_postgres_execute(self, query_str: str, args: Tuple[Any, ...]) -> int:
        import psycopg

        psycopg_module: Any = cast(Any, psycopg)
        with psycopg_module.connect(self._get_postgres_conninfo()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_str, args)
                return int(cursor.rowcount)


# Instância única da classe Database
db: Database = Database()