"""
Script de exportação de emissões para CSV / Excel.

Utiliza a camada de serviço (emission_service) e a biblioteca padrão `csv` do Python,
sendo 100% agnóstico ao banco de dados (SQLite ou PostgreSQL) e sem dependências pesadas.
"""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

# Adiciona a raiz do projeto ao path caso o script seja executado diretamente
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.services.emission_service import emission_service


def export_data(output_directory: Path | None = None) -> Path | None:
    """
    Exporta todos os registros de emissão para um arquivo CSV formatado para o Excel.

    Args:
        output_directory: Diretório onde o arquivo será salvo. Se None, usa Documents/Emissions.

    Returns:
        Path do arquivo gerado ou None se não houver registros.
    """
    print("Iniciando exportação de registros de emissões...")

    records: List[Dict[str, Any]] = emission_service.get_export_records()

    if not records:
        print("⚠️ A tabela de emissões está vazia. Nenhum arquivo gerado.")
        return None

    # Define o diretório de saída
    if output_directory is None:
        docs_dir = Path.home() / "Documents" / "Emissions"
        try:
            docs_dir.mkdir(parents=True, exist_ok=True)
            target_dir = docs_dir
        except Exception:
            # Fallback para o diretório local se Documents não estiver acessível
            target_dir = current_dir
    else:
        target_dir = output_directory
        target_dir.mkdir(parents=True, exist_ok=True)

    today_str: str = date.today().strftime('%Y-%m-%d')
    file_name: str = f"emissions_{today_str}.csv"
    output_path: Path = target_dir / file_name

    # Cabeçalhos amigáveis em português para a planilha
    fieldnames = [
        ('id_record', 'ID'),
        ('emission_amount', 'Emissão (kg CO₂)'),
        ('distance', 'Distância (km)'),
        ('people_amount', 'Passageiros'),
        ('vehicle', 'Veículo'),
        ('fuel', 'Combustível'),
        ('created_at', 'Data e Hora')
    ]

    try:
        # utf-8-sig inclui o BOM (Byte Order Mark), fazendo o Excel no Windows abrir com acentos perfeitos
        with open(output_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            # Escreve o cabeçalho
            writer.writerow([label for _, label in fieldnames])

            # Escreve cada registro
            for r in records:
                writer.writerow([
                    r.get('id_record', ''),
                    str(r.get('emission_amount', '')).replace('.', ','),
                    str(r.get('distance', '')).replace('.', ','),
                    r.get('people_amount') if r.get('people_amount') is not None else 'Ind.',
                    r.get('vehicle', ''),
                    r.get('fuel', ''),
                    r.get('created_at', '')
                ])

        print(f"✓ {len(records)} registros exportados com sucesso!")
        print(f"📁 Arquivo salvo em: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    export_data()
