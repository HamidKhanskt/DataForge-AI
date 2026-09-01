import pandas as pd
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@tool
def detect_duplicate_orders(filename: str) -> dict:
    """Detect duplicate order_id rows, which can indicate duplicate charges."""

    path = PROJECT_ROOT / filename

    if not path.exists():
        return {
            "status": "error",
            "error": f"Dataset not found: {filename}",
        }

    df = pd.read_csv(path)

    if "order_id" not in df.columns:
        return {
            "status": "error",
            "error": "Column 'order_id' not found in dataset",
        }

    dupes = df[df.duplicated(subset=["order_id"], keep=False)]

    groups = []

    for order_id, group  in dupes.groupby("order_id"):
        groups.append(
            {
                "order_id": int(order_id),
                "occurrences": int(len(group)),
                "rows": group.index.tolist(),
            }
        )

    return {
        "status": "success",
        "dataset": filename,
        "duplicate_groups": groups,
        "duplicate_group_count": len(groups),
        "duplicate_row_count": int(len(dupes)),
    }
