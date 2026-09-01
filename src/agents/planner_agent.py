from typing import Dict, Any


def planner_agent(question: str) -> Dict[str, Any]:
    """Create a deterministic investigation plan for a data-quality task."""

    question_lower = question.lower()

    checks = []

    if "duplicate" in question_lower:
        checks.append("duplicate_detection")

    if any(word in question_lower for word in [
        "quality",
        "missing",
        "null",
        "invalid",
        "anomaly",
        "anomalies",
    ]):
        checks.append("anomaly_detection")

    if any(word in question_lower for word in [
        "business",
        "rule",
        "rules",
        "violation",
        "violations",
    ]):
        checks.append("business_rule_validation")

    if any(word in question_lower for word in [
        "insight",
        "insights",
        "trend",
        "analysis",
        "analyze",
    ]):
        checks.append("business_insights")

    if not checks:
        checks = [
            "duplicate_detection",
            "anomaly_detection",
            "business_rule_validation",
            "business_insights",
        ]

    return {
        "status": "success",
        "question": question,
        "plan": checks,
        "step_count": len(checks),
    }

