import pandas as pd
from pathlib import Path
from langchain_core.tools import tool

DATA_ROOT = Path(__file__).resolve().parents[2] / "data" / "raw"

@tool
def inspect_dataset(filename: str) -> dict:
    """Inspect a CSV dataset."""
    file_path = DATA_ROOT / filename
    if not file_path.exists():
        return {"status": "error", "error": f"Dataset not found: {filename}"}
    df = pd.read_csv(file_path)
    return {"status": "success", "dataset": filename, "rows": int(len(df)), "columns": int(len(df.columns)), "column_names": list(df.columns), "data_types": {column: str(dtype) for column, dtype in df.dtypes.items()}, "missing_values": {column: int(count) for column, count in df.isna().sum().items() if count > 0}, "duplicate_rows": int(df.duplicated().sum())}
