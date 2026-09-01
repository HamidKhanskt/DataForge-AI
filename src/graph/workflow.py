from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import json

from src.tools.anomaly_tools import detect_numeric_anomalies
from src.tools.business_rules import validate_order_totals
from src.tools.duplicate_tools import detect_duplicate_orders

from src.agents.planner_agent import planner_agent
from src.agents.diagnosis_agent import diagnose_incident
from src.agents.evaluator import evaluate_diagnosis
from src.agents.severity_agent import classify_severity


class DataForgeState(TypedDict, total=False):
    incident: str
    plan: list
    evidence: dict
    diagnosis: str
    evaluation: dict
    severity: str
    status: str
    filename: str


def planning_node(state: DataForgeState):
    """
    Planner determines which investigation checks are relevant
    to the user's incident/question.
    """

    result = planner_agent(state["incident"])

    return {
        "plan": result["plan"],
        "status": "planned",
    }


def investigate_node(state: DataForgeState):
    """
    Execute the investigation tools selected by the planner.
    """

    filename = state["filename"]
    plan = state.get("plan", [])

    evidence = {}

    # Numerical anomaly detection
    if "anomaly_detection" in plan:
        evidence["anomalies"] = detect_numeric_anomalies.invoke(
            {
                "filename": filename
            }
        )

    # Business-rule validation
    if "business_rule_validation" in plan:
        evidence["business_rules"] = validate_order_totals.invoke(
            {
                "filename": filename
            }
        )

    # Duplicate detection
    if "duplicate_detection" in plan:
        evidence["duplicates"] = detect_duplicate_orders.invoke(
            {
                "filename": filename
            }
        )

    return {
        "evidence": evidence,
        "status": "investigated",
    }


def severity_node(state: DataForgeState):
    """
    Deterministically classify incident severity from collected evidence.

    This severity is authoritative and is passed to the diagnosis agent.
    """

    severity = classify_severity(
        state["evidence"]
    )

    return {
        "severity": severity,
        "status": "severity_classified",
    }


def diagnosis_node(state: DataForgeState):
    """
    Generate an evidence-driven root-cause analysis.

    The deterministic severity is explicitly passed to the LLM so the
    diagnosis cannot contradict the authoritative severity classification.
    """

    evidence = json.dumps(
        state["evidence"],
        indent=2,
    )

    result = diagnose_incident(
        state["incident"],
        evidence,
        state["severity"],
    )

    return {
        "diagnosis": result.content,
        "status": "diagnosed",
    }


def evaluation_node(state: DataForgeState):
    """
    Evaluate whether the diagnosis is supported by the collected evidence.
    """

    evaluation = evaluate_diagnosis(
        state["evidence"],
        state["diagnosis"],
    )

    return {
        "evaluation": evaluation,
        "status": "evaluated",
    }


# ---------------------------------------------------------
# Build DataForge LangGraph workflow
# ---------------------------------------------------------

builder = StateGraph(DataForgeState)

# Nodes
builder.add_node(
    "plan",
    planning_node,
)

builder.add_node(
    "investigate",
    investigate_node,
)

builder.add_node(
    "severity",
    severity_node,
)

builder.add_node(
    "diagnosis",
    diagnosis_node,
)

builder.add_node(
    "evaluate",
    evaluation_node,
)

# Workflow edges
builder.add_edge(
    START,
    "plan",
)

builder.add_edge(
    "plan",
    "investigate",
)

builder.add_edge(
    "investigate",
    "severity",
)

builder.add_edge(
    "severity",
    "diagnosis",
)

builder.add_edge(
    "diagnosis",
    "evaluate",
)

builder.add_edge(
    "evaluate",
    END,
)


# Compile the graph
research_graph = builder.compile()
