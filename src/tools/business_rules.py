import pandas as pd
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@tool
def validate_order_totals(filename: str) -> dict:
    """Validate order totals against quantity multiplied by unit price."""

    path = PROJECT_ROOT / filename

    if not path.exists():
        return {
            "status": "error",
            "error": f"Dataset not found: {filename}",
        }

    df = pd.read_csv(path)

    expected = df["quantity"] * df["unit_price"]
    difference = (df["order_total"] - expected).round(2)

    invalid = df[difference.abs() > 0.01]

    violations = []

    for index, row in invalid.iterrows():
        violations.append(
            {
                "row": int(index),
                "order_id": int(row["order_id"]),
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "reported_total": float(row["order_total"]),
                "expected_total": float(expected.loc[index]),
                "difference": float(difference.loc[index]),
            }
        )

    return {
        "status": "success",
        "dataset": filename,
        "rule": "order_total = quantity * unit_price",
        "violations": violations,
        "violation_count": len(violations),
    }
