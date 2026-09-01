from typing import Dict, Any

def classify_severity(evidence: Dict[str, Any]) -> str:
    anomalies = evidence.get("anomalies", {})
    business_rules = evidence.get("business_rules", {})
    anomaly_results = anomalies.get("anomalies", {})
    violations = business_rules.get("violations", [])
    anomaly_count = sum(item.get("count", 0) for item in anomaly_results.values())
    violation_count = len(violations)
    if violation_count >= 5 or anomaly_count >= 5:
        return "CRITICAL"
    if violation_count >= 2 or anomaly_count >= 2:
        return "HIGH"
    if violation_count == 1 or anomaly_count == 1:
        return "MEDIUM"
    return "LOW"
