import json
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from pydantic import ValidationError

# tentar importar rich de forma opcional (evita ModuleNotFoundError em ambientes sem dependências instaladas)
try:
    from rich.console import Console
    console = Console()
except Exception:
    console = None

from models import RowModel

def process_file(input_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Lê um CSV, valida linhas com RowModel, salva valid.csv e report.json no output_dir.
    Retorna dicionário resumo.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    total = len(df)
    valid_rows: List[Dict[str, Any]] = []
    invalids: List[Dict[str, Any]] = []

    for idx, row in df.iterrows():
        data = row.to_dict()
        try:
            model = RowModel.parse_obj(data)
            valid_rows.append(model.dict())
        except ValidationError as e:
            invalids.append({
                "index": int(idx),
                "row": data,
                "errors": e.errors()
            })

    # salvar valid rows
    if valid_rows:
        valid_df = pd.DataFrame(valid_rows)
        valid_path = output_dir / "valid.csv"
        valid_df.to_csv(valid_path, index=False)
    else:
        valid_path = output_dir / "valid.csv"
        # criar arquivo vazio com cabeçalho baseado no modelo
        pd.DataFrame(columns=["id", "name", "email", "age"]).to_csv(valid_path, index=False)

    # relatório
    report = {
        "input_file": str(input_path),
        "total_rows": total,
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalids),
        "invalid_details": invalids
    }
    report_path = output_dir / "report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # usar rich se disponível, senão print simples
    if console:
        console.print(f"[green]Process completed[/green]: {total} rows -> {len(valid_rows)} valid, {len(invalids)} invalid")
        console.print(f"[blue]Outputs[/blue]: {valid_path}, {report_path}")
    else:
        print(f"Process completed: {total} rows -> {len(valid_rows)} valid, {len(invalids)} invalid")
        print(f"Outputs: {valid_path}, {report_path}")

    return {
        "valid_path": str(valid_path),
        "report_path": str(report_path),
        "summary": report
    }
