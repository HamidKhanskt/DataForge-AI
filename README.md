# ⚡ DataForge AI

### Autonomous Data Investigation & Root Cause Analysis

> **DataForge AI is an agentic data reliability platform that autonomously investigates CSV datasets, detects data-quality issues, validates business rules, identifies anomalies and duplicates, evaluates evidence, determines incident severity, and generates an explainable root-cause investigation report.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Orchestration-1C3C3C?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge\&logo=langchain\&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)

</p>

---

## 🎯 Why DataForge AI?

Modern data teams spend significant time investigating incidents such as:

* 📊 Unexpected revenue changes
* ❌ Broken business rules
* 🔢 Numerical anomalies
* 🔁 Duplicate records
* 🧹 Data-quality problems
* 🚨 Production data incidents
* 🔍 Unknown root causes

Traditional data-quality scripts can identify problems, but they usually stop at **detection**.

DataForge AI goes further.

It combines deterministic data-quality tools with an agentic investigation workflow that can:

**Plan → Investigate → Collect Evidence → Classify Severity → Diagnose → Evaluate → Report**

---

# 🧠 Agentic Architecture

```text
                         ┌──────────────────────────┐
                         │       USER REQUEST       │
                         │                          │
                         │ "Investigate this data   │
                         │  for quality problems"   │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │      PLANNER AGENT       │
                         │                          │
                         │ Determines which checks │
                         │ are required             │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                  ┌────────────────────────────────────────┐
                  │          INVESTIGATION LAYER           │
                  │                                        │
                  │  ┌──────────────┐  ┌───────────────┐  │
                  │  │ Duplicate    │  │   Anomaly     │  │
                  │  │ Detection    │  │   Detection   │  │
                  │  └──────────────┘  └───────────────┘  │
                  │                                        │
                  │  ┌──────────────────────────────────┐  │
                  │  │      Business Rule Validation     │  │
                  │  └──────────────────────────────────┘  │
                  └────────────────────┬───────────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │       EVIDENCE STATE     │
                         │                          │
                         │ Structured investigation │
                         │ results + findings       │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │    SEVERITY AGENT        │
                         │                          │
                         │ LOW / MEDIUM / HIGH /   │
                         │ CRITICAL                 │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │     DIAGNOSIS AGENT      │
                         │                          │
                         │ Root cause + evidence + │
                         │ remediation              │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │      EVALUATOR           │
                         │                          │
                         │ Validates whether the   │
                         │ evidence supports the   │
                         │ investigation             │
                         └─────────────┬────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │      INCIDENT REPORT     │
                         │                          │
                         │ Findings • Severity •   │
                         │ Diagnosis • Remediation │
                         └──────────────────────────┘
```

---

# 🤖 Why This Is Agentic AI

DataForge is not simply an LLM wrapped around a CSV.

The system uses **multiple specialized components with distinct responsibilities**.

### 🧭 Planner

Analyzes the investigation request and creates an investigation plan.

Example:

```text
User Request
     ↓
Planner
     ↓
├── Duplicate Detection
├── Anomaly Detection
├── Business Rule Validation
└── Business Insights
```

The investigation is therefore **request-driven**, rather than executing the exact same fixed analysis every time.

---

### 🔎 Investigation Tools

The agents call deterministic Python tools to obtain factual evidence.

Examples:

* `detect_duplicate_orders`
* `detect_numeric_anomalies`
* `validate_order_totals`

The LLM does **not invent the evidence**.

The tools inspect the actual dataset.

---

### 🚨 Severity Classification

Evidence is converted into an incident severity:

```text
LOW
 ↓
MEDIUM
 ↓
HIGH
 ↓
CRITICAL
```

Severity is determined from detected anomalies and business-rule violations.

---

### 🧠 Diagnosis Agent

A local LLM analyzes the collected evidence and produces:

* Root-cause hypothesis
* Evidence explanation
* Confidence estimate
* Remediation recommendations
* Prevention recommendations

The diagnosis is explicitly instructed to use **only supplied evidence**.

---

### ✅ Evaluator

The system evaluates whether the evidence collection succeeded and whether the investigation has sufficient evidence to be accepted.

Example:

```text
Evidence
   ↓
Validation
   ↓
┌───────────────┐
│ Evidence OK?  │
└───────┬───────┘
        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
ACCEPTED   REJECTED
```

This creates an important reliability layer instead of blindly trusting the LLM.

---

# 🔧 Tool Calling

DataForge uses deterministic tools for factual investigation.

```text
                 DataForge Agent
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Duplicate      Anomaly      Business
     Detection     Detection       Rules
          │            │            │
          └────────────┼────────────┘
                       ▼
                  Evidence
```

### Example

For an order:

```text
quantity = 2
unit_price = $25
reported_total = $75
```

DataForge calculates:

```text
Expected = 2 × $25
         = $50
```

Then detects:

```text
Reported = $75
Expected = $50

Difference = +$25
```

The LLM receives this evidence and explains the incident.

---

# 🔄 LangGraph Workflow

The core orchestration is implemented with LangGraph.

```text
START
  │
  ▼
PLAN
  │
  ▼
INVESTIGATE
  │
  ▼
SEVERITY
  │
  ▼
DIAGNOSIS
  │
  ▼
EVALUATE
  │
  ▼
 END
```

The shared state contains information such as:

```text
incident
plan
filename
evidence
severity
diagnosis
evaluation
status
```

This allows each stage to consume and enrich the investigation state.

---

# 📊 Example Investigation

Given an orders dataset, DataForge can identify:

### ⚠️ Numerical Anomaly

```text
unit_price = $600
```

### ❌ Business Rule Violations

```text
Order 1001

Quantity:        2
Unit Price:      $25
Reported Total:  $75
Expected Total:  $50

Difference:      +$25
```

```text
Order 1002

Quantity:        1
Unit Price:      $600
Reported Total:  $120
Expected Total:  $600

Difference:      -$480
```

### 🔁 Duplicate Detection

```text
Duplicate Orders: 0
```

DataForge then combines these findings into an investigation and produces a root-cause assessment.

---

# 💰 Financial Impact Analysis

The platform can surface discrepancies between reported and expected revenue.

Example:

```text
Expected Revenue      $650
Reported Revenue      $195
────────────────────────────
Net Revenue Impact   -$455
```

Affected-order discrepancy:

```text
Order 1001    +$25
Order 1002   -$480
──────────────────
Gross         $505
```

This makes the output useful not only for engineers, but also for **data analysts, operations teams, and business stakeholders**.

---

# 🖥️ Streamlit Interface

DataForge includes a Streamlit interface for running investigations interactively.

### Interface capabilities

* 📤 Upload CSV datasets
* 👀 Preview uploaded data
* 🧠 Enter natural-language investigation requests
* 📋 View the generated investigation plan
* 🔎 View structured evidence
* ⚠️ View anomalies
* ❌ View business-rule violations
* 💰 View financial impact
* 🚨 View severity
* 🧠 View root-cause analysis
* ✅ View evaluation results
* 📄 Generate an incident report

The UI is designed to present **investigation results instead of raw Python objects**, making the application suitable for demonstrations and portfolio use.

---

# 🧱 Project Structure

```text
DataForge-AI/
│
├── app/
│   └── streamlit_app.py
│
├── src/
│   │
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── diagnosis_agent.py
│   │   ├── severity_agent.py
│   │   └── evaluator.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── tools/
│   │   ├── duplicate_tools.py
│   │   ├── anomaly_tools.py
│   │   └── business_rules.py
│   │
│   └── reports/
│       └── report_generator.py
│
├── data/
│   └── raw/
│       └── orders.csv
│
├── reports/
│   └── incident_report.md
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| 🐍 Python     | Core application             |
| 🦜 LangChain  | LLM application framework    |
| 🕸️ LangGraph | Agent/workflow orchestration |
| 🦙 Ollama     | Local LLM inference          |
| 🧠 Llama 3.2  | Diagnosis/reasoning          |
| 📊 Pandas     | Dataset analysis             |
| 🎈 Streamlit  | Interactive UI               |
| 🧪 Pytest     | Testing                      |
| 📄 Markdown   | Investigation reports        |

---

# 🔐 Reliability Philosophy

DataForge follows an important principle:

> **LLMs explain evidence; deterministic tools produce evidence.**

This separation helps reduce hallucinations.

Instead of asking an LLM:

```text
"Are there duplicate orders?"
```

and trusting its answer, DataForge calls a deterministic duplicate-detection tool.

The resulting evidence is then passed to the diagnosis agent.

```text
CSV
 │
 ▼
Deterministic Tools
 │
 ▼
Structured Evidence
 │
 ▼
LLM Diagnosis
 │
 ▼
Evaluation
```

---

# 🧪 Validation

The project includes validation for core components.

Example tool execution:

```text
Duplicate Detection
────────────────────
Status: SUCCESS
Duplicate Groups: 0
Duplicate Rows:   0
```

Workflow validation:

```text
START
  ↓
PLAN
  ↓
INVESTIGATE
  ↓
SEVERITY
  ↓
DIAGNOSIS
  ↓
EVALUATE
  ↓
END
```

The LangGraph workflow compiles successfully before execution.

---

# 🚀 Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DataForge-AI.git
cd DataForge-AI
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start Ollama

Make sure Ollama is running and the required model is available:

```bash
ollama pull llama3.2
```

## 5. Launch DataForge

```bash
streamlit run app/streamlit_app.py
```

Then open the Streamlit URL shown in your terminal.

---

# 🧑‍💻 Example Investigation Requests

Try asking DataForge:

### Basic

```text
Analyze this dataset for duplicate orders and data quality issues.
```

### Advanced

```text
Investigate this orders dataset for anomalies, duplicate records, 
business-rule violations, revenue discrepancies, and determine 
the most likely root cause with evidence-backed remediation steps.
```

### Incident-style

```text
Revenue reporting appears inconsistent with the underlying orders.
Investigate the dataset, identify all relevant data-quality failures,
quantify the financial impact, determine the severity, and provide
an evidence-backed root-cause assessment and remediation plan.
```

---

# 📈 Future Roadmap

DataForge is designed to evolve into a broader **AI Data Reliability Platform**.

### Planned capabilities

* [ ] 🔌 Database connectors
* [ ] ☁️ Cloud storage support
* [ ] 📊 Automatic profiling
* [ ] 📈 Trend detection
* [ ] 🔍 Schema drift detection
* [ ] 🧪 Data-quality test generation
* [ ] 📝 SQL investigation agent
* [ ] 🗄️ SQL database tools
* [ ] 🔄 Automatic remediation proposals
* [ ] 📡 Production monitoring
* [ ] 🔔 Incident alerting
* [ ] 🧠 Multi-agent investigation
* [ ] 📚 Historical incident memory
* [ ] 📊 Investigation dashboards
* [ ] 🧪 LLM evaluation benchmarks

---

# 💡 What This Project Demonstrates

DataForge AI demonstrates practical experience with:

**Agentic AI**
→ Planning, orchestration, specialized agents

**LangGraph**
→ Stateful multi-step workflows

**LangChain**
→ LLM integration and structured agent components

**Tool Calling**
→ Deterministic Python tools for evidence collection

**RAG/AI Reliability Principles**
→ Separating factual evidence from LLM reasoning

**Data Engineering**
→ Data validation, anomaly detection, business rules

**LLM Applications**
→ Evidence-grounded diagnosis and remediation

**Production Thinking**
→ Evaluation, severity classification, reports, and UI

---

# 👨‍💻 Author

**Hamid Khan**

AI / ML Engineer focused on:

* 🤖 Agentic AI
* 🧠 LLM Applications
* 🔗 LangChain
* 🕸️ LangGraph
* 📚 RAG
* 👁️ Computer Vision
* 🐍 Python
* 📊 Data & AI Engineering

---

## ⭐ Project Philosophy

> **Don't just ask an LLM what went wrong. Give it tools, evidence, state, and an evaluation layer — then make it explain its reasoning.**

**DataForge AI turns raw data incidents into structured, evidence-backed investigations.**

⭐ If you find the project interesting, consider starring the repository.
