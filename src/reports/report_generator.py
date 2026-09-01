from pathlib import Path


def generate_report(state: dict) -> str:
    evidence = state.get("evidence", {})
    evaluation = state.get("evaluation", {})
    diagnosis = state.get("diagnosis", "")
    severity = state.get("severity", "UNKNOWN")

    lines = []
    lines.append("# DataForge Incident Report")
    lines.append("")
    lines.append(f"Severity: {severity}")
    lines.append(f"Evaluation: {evaluation.get('status', 'unknown').upper()}")
    lines.append(f"Score: {evaluation.get('score', 0.0)}")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    lines.append(str(evidence))
    lines.append("")
    lines.append("## Diagnosis")
    lines.append("")
    lines.append(diagnosis)

    report = "\n".join(lines)
    Path("reports/incident_report.md").write_text(report)
    return report
