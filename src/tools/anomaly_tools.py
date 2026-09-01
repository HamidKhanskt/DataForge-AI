import pandas as pd
from pathlib import Path
from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@tool
def detect_numeric_anomalies(filename: str) -> dict:
    """Detect numeric outliers using the IQR method."""

    path = PROJECT_ROOT / filename

    if not path.exists():
        return {
            "status": "error",
            "error": f"Dataset not found: {filename}",
        }

    df = pd.read_csv(path)

    result = {}

    for column in df.select_dtypes(include="number").columns:
        s = df[column].dropna()

        if len(s) < 4:
            continue

        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1

        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr

        values = s[(s < low) | (s > high)]

        if len(values):
            result[column] = {
                "count": int(len(values)),
                "values": values.tolist(),
            }

    return {
        "status": "success",
        "dataset": filename,
        "anomalies": result,
    }
