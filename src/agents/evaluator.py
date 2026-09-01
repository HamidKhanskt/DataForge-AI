from typing import Dict, Any


def evaluate_diagnosis(
    evidence: Dict[str, Any],
    diagnosis: str
) -> Dict[str, Any]:

    anomalies = evidence.get("anomalies", {})
    business_rules = evidence.get("business_rules", {})

    anomaly_ok = anomalies.get("status") == "success"
    rules_ok = business_rules.get("status") == "success"

    anomaly_results = anomalies.get("anomalies", {})
    violations = business_rules.get("violations", [])

    has_anomalies = bool(anomaly_results)
    has_violations = bool(violations)

    evidence_valid = anomaly_ok and rules_ok

    if not evidence_valid:
        return {
            "status": "rejected",
            "score": 0.0,
            "reason": "Evidence collection failed.",
            "has_anomalies": has_anomalies,
            "has_business_rule_violations": has_violations,
        }

    if has_anomalies or has_violations:
        return {
            "status": "accepted",
            "score": 1.0,
            "reason": "Evidence confirms detected data-quality issues.",
            "has_anomalies": has_anomalies,
            "has_business_rule_violations": has_violations,
        }

    return {
        "status": "accepted",
        "score": 1.0,
        "reason": "Evidence confirms no detected data-quality issues.",
        "has_anomalies": False,
        "has_business_rule_violations": False,
    }
