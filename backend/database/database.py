"""
Módulo de abstração e conexão com o banco de dados.

Este script é responsável por toda a interação com o banco de dados PostgreSQL.
Ele utiliza a biblioteca python-dotenv para carregar as credenciais de um arquivo .env,
oferece uma classe `Database` que gerencia as conexões e simplifica a execução
de queries, e exporta uma instância única `db` para ser usada em toda a aplicação.
"""

import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Garante que as variáveis de ambiente do arquivo .env sejam carregadas
# assim que o módulo for importado.
load_dotenv()


class Database:
    """
    Classe handler para gerenciar a conexão e as operações com o banco de dados.

    Esta classe encapsula a lógica de conexão com o PostgreSQL, lendo as
    credenciais das variáveis de ambiente. Seu principal objetivo é fornecer um
    método `query` simplificado para executar comandos SQL de forma segura,
    gerenciando o ciclo de vida da conexão e do cursor automaticamente.
    """

    def __init__(self):
        """
        Inicializa a instância da classe Database.

        O construtor lê as variáveis de ambiente necessárias para a conexão
        com o banco de dados (DB_HOST, DB_USER, etc.) e as armazena em um
        dicionário de parâmetros (`self.db_params`) que será usado para
        estabelecer futuras conexões.
        """
        self.db_params = {
            'dbname': os.environ.get('POSTGRESQL_DB_NAME'),
            'user': os.environ.get('POSTGRESQL_USER'),
            'password': os.environ.get('POSTGRESQL_PASSWORD'),
            'host': os.environ.get('POSTGRESQL_HOST'),
            'port': os.environ.get('POSTGRESQL_PORT')
        }

    def query(self, query: str, args: tuple = None):
        """
        Executa uma query SQL no banco de dados de forma segura.

        Este método abre uma conexão, executa a query fornecida e fecha a
        conexão. Ele usa parâmetros para prevenir ataques de SQL Injection.
        O comportamento do retorno varia de acordo com o tipo de query executada.
        Graças ao `row_factory=dict_row`, consultas SELECT retornam uma lista de
        dicionários, o que facilita a manipulação dos dados e a serialização para JSON.

        Args:
            query (str): A string da query SQL a ser executada.
                         Use '%s' como placeholder para os parâmetros.
            args (tuple, optional): Uma tupla contendo os valores para substituir
                                    os placeholders na query. Defaults to None.

        Raises:
            psycopg.Error: Captura qualquer exceção relacionada ao banco de dados
                           (ex: erro de sintaxe SQL, falha de conexão).

        Returns:
            list[dict]: Para queries `SELECT`, retorna uma lista de dicionários,
                        onde cada dicionário representa uma linha do resultado.
            int: Para queries `INSERT`, `UPDATE` ou `DELETE`, retorna o número
                 de linhas afetadas pela operação.
        """
        # A instrução 'with' garante que a conexão será fechada automaticamente
        # ao final do bloco, mesmo que ocorram erros.
        with psycopg.connect(**self.db_params, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, args)

                # Verifica se a query é um SELECT para decidir o que retornar
                if query.strip().lower().startswith('select'):
                    return cursor.fetchall()

                # Para outras operações, retorna o número de linhas afetadas
                return cursor.rowcount


# Instância única (singleton-like) da classe Database.
# Outros módulos da aplicação devem importar esta variável `db` para interagir
# com o banco de dados, garantindo que a configuração seja carregada uma única vez.
db = Database()