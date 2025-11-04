import pandas as pd
import sqlalchemy
from pathlib import Path
from datetime import date
import sys

DB_USER = "postgres"
DB_PASS = "seu_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "seu_banco_de_dados"

SQL_QUERY = "SELECT * FROM public.emission_records ORDER BY id_record;"

file_name = f"{date.today().strftime('%Y-%m-%d')}.xlsm"

output_dir = Path.home() / "Documents" / "Emissions"
output_path = output_dir / file_name


def export_data():
    print("Iniciando script de exportação de emissões...")
    
    try:
        print(f"Conectando ao banco '{DB_NAME}' em '{DB_HOST}'...")

        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = sqlalchemy.create_engine(connection_string)

        print("Buscando dados da tabela 'emission_records'...")
        df = pd.read_sql(SQL_QUERY, engine)
        
        if df.empty:
            print("A tabela está vazia. Nenhum arquivo será gerado.")
            return

        print(f"Encontrados {len(df)} registros.")

        print(f"Verificando pasta de destino: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Salvando arquivo em: {output_path}")
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print("\n--- SUCESSO! ---")
        print(f"Arquivo salvo com sucesso em {output_path}")

    except sqlalchemy.exc.OperationalError as e:
        print("\n--- ERRO DE CONEXÃO ---", file=sys.stderr)
        print("Falha ao conectar no PostgreSQL. Verifique suas credenciais (usuário, senha, nome do banco) no script.", file=sys.stderr)
    except Exception as e:
        print(f"\n--- UM ERRO INESPERADO OCORREU ---", file=sys.stderr)
        print(e, file=sys.stderr)

if __name__ == "__main__":
    export_data()
