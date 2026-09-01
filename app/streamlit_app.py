import os
import sys
import tempfile

if "." not in sys.path:
    sys.path.insert(0, ".")

import pandas as pd
import streamlit as st

from src.graph.workflow import research_graph
from src.reports.report_generator import generate_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DataForge AI",
    page_icon="🔎",
    layout="wide",
)


# =========================================================
# HEADER
# =========================================================

st.title("DataForge AI")
st.markdown(
    "**Autonomous Data Investigation & Root Cause Analysis**"
)

st.divider()


# =========================================================
# DATASET
# =========================================================

st.subheader("Dataset")

default_dataset = "data/raw/orders.csv"

uploaded_file = st.file_uploader(
    "Upload a CSV dataset (optional)",
    type=["csv"],
)

if uploaded_file is not None:

    temp_dir = tempfile.mkdtemp()

    dataset_path = os.path.join(
        temp_dir,
        uploaded_file.name,
    )

    with open(dataset_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    dataset_name = uploaded_file.name

else:

    dataset_path = default_dataset
    dataset_name = os.path.basename(default_dataset)


# =========================================================
# DATASET PREVIEW
# =========================================================

if not os.path.exists(dataset_path):

    st.error(
        f"Dataset not found: {dataset_path}"
    )

    st.info(
        "Upload a CSV dataset above."
    )

    st.stop()


try:

    df = pd.read_csv(dataset_path)

except Exception as e:

    st.error(
        f"Unable to read dataset: {e}"
    )

    st.stop()


st.success(
    f"Dataset ready: **{dataset_name}**"
)

c1, c2 = st.columns(2)

c1.metric(
    "ROWS",
    f"{len(df):,}",
)

c2.metric(
    "COLUMNS",
    f"{len(df.columns):,}",
)


with st.expander("Preview Dataset"):

    st.dataframe(
        df.head(10),
        use_container_width=True,
    )


# =========================================================
# INVESTIGATION REQUEST
# =========================================================

st.subheader("Investigation Request")

incident = st.text_area(
    "What should DataForge investigate?",
    value=(
        "Investigate this dataset as if it were being used "
        "for an executive revenue report. Determine whether "
        "the reported revenue is trustworthy. Correlate "
        "anomalies, duplicate records, and business-rule "
        "violations; quantify the financial impact; identify "
        "affected records; distinguish confirmed evidence "
        "from root-cause hypotheses; assess business risk; "
        "and provide prioritized remediation and prevention "
        "recommendations. Do not assume a root cause that "
        "cannot be supported by evidence."
    ),
    height=160,
)


# =========================================================
# RUN DATAFORGE
# =========================================================

if st.button(
    "🔎 Run DataForge",
    type="primary",
    use_container_width=True,
):

    if not incident.strip():

        st.warning(
            "Please enter an investigation request."
        )

        st.stop()


    with st.spinner(
        "DataForge AI is investigating..."
    ):

        try:

            result = research_graph.invoke(
                {
                    "incident": incident,
                    "filename": dataset_path,
                }
            )

        except Exception as e:

            st.error(
                f"Investigation failed: {e}"
            )

            st.stop()


    # =====================================================
    # EXTRACT RESULTS
    # =====================================================

    evidence = result.get(
        "evidence",
        {},
    )

    evaluation = result.get(
        "evaluation",
        {},
    )

    anomalies = evidence.get(
        "anomalies",
        {},
    )

    business_rules = evidence.get(
        "business_rules",
        {},
    )

    duplicates = evidence.get(
        "duplicates",
        {},
    )

    anomaly_data = anomalies.get(
        "anomalies",
        {},
    )

    violations = business_rules.get(
        "violations",
        [],
    )

    duplicate_groups = duplicates.get(
        "duplicate_group_count",
        0,
    )

    anomaly_count = sum(
        item.get("count", 0)
        for item in anomaly_data.values()
    )


    # =====================================================
    # INVESTIGATION COMPLETED
    # =====================================================

    st.success(
        "Investigation completed successfully."
    )


    # =====================================================
    # SUMMARY
    # =====================================================

    st.subheader(
        "Investigation Summary"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "STATUS",
        result.get(
            "status",
            "-"
        ).upper(),
    )

    c2.metric(
        "SEVERITY",
        result.get(
            "severity",
            "-"
        ),
    )

    c3.metric(
        "ANOMALIES",
        anomaly_count,
    )

    c4.metric(
        "RULE VIOLATIONS",
        len(violations),
    )


    # =====================================================
    # INVESTIGATION PLAN
    # =====================================================

    plan = result.get(
        "plan",
        [],
    )

    if plan:

        st.subheader(
            "Investigation Plan"
        )

        plan_labels = {
            "duplicate_detection":
                "Duplicate Detection",

            "anomaly_detection":
                "Anomaly Detection",

            "business_rule_validation":
                "Business Rule Validation",

            "business_insights":
                "Business Insights",
        }

        for step in plan:

            label = plan_labels.get(
                step,
                step.replace(
                    "_",
                    " ",
                ).title(),
            )

            st.markdown(
                f"✓ **{label}**"
            )


    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.subheader(
        "Key Findings"
    )

    if anomaly_count > 0:

        st.warning(
            f"⚠️ {anomaly_count} numerical anomaly/anomalies detected."
        )

    else:

        st.success(
            "✓ No numerical anomalies detected."
        )


    if violations:

        st.error(
            f"❌ {len(violations)} business-rule violation(s) detected."
        )

    else:

        st.success(
            "✓ No business-rule violations detected."
        )


    if duplicate_groups > 0:

        st.warning(
            f"⚠️ {duplicate_groups} duplicate group(s) detected."
        )

    else:

        st.success(
            "✓ No duplicate orders detected."
        )


    # =====================================================
    # ANOMALIES
    # =====================================================

    if anomaly_data:

        st.subheader(
            "Anomalies"
        )

        for column, details in anomaly_data.items():

            count = details.get(
                "count",
                0,
            )

            values = details.get(
                "values",
                [],
            )

            st.markdown(
                f"**{column}** — {count} anomalous value(s)"
            )

            if values:

                st.write(
                    "Detected values:",
                    ", ".join(
                        str(v)
                        for v in values
                    ),
                )


    # =====================================================
    # BUSINESS RULE VIOLATIONS
    # =====================================================

    if violations:

        st.subheader(
            "Business-Rule Violations"
        )

        for violation in violations:

            order_id = violation.get(
                "order_id",
                "Unknown",
            )

            quantity = violation.get(
                "quantity",
                0,
            )

            unit_price = violation.get(
                "unit_price",
                0,
            )

            reported_total = violation.get(
                "reported_total",
                0,
            )

            expected_total = violation.get(
                "expected_total",
                0,
            )

            difference = violation.get(
                "difference",
                0,
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### Order {order_id}"
                )

                a, b, c = st.columns(3)

                a.metric(
                    "Quantity",
                    quantity,
                )

                b.metric(
                    "Unit Price",
                    f"${unit_price:,.2f}",
                )

                c.metric(
                    "Reported Total",
                    f"${reported_total:,.2f}",
                )

                a.metric(
                    "Expected Total",
                    f"${expected_total:,.2f}",
                )

                b.metric(
                    "Difference",
                    f"${difference:,.2f}",
                )


    # =====================================================
    # FINANCIAL IMPACT
    # =====================================================

    if violations:

        expected_revenue = sum(
            float(
                v.get(
                    "expected_total",
                    0,
                )
            )
            for v in violations
        )

        reported_revenue = sum(
            float(
                v.get(
                    "reported_total",
                    0,
                )
            )
            for v in violations
        )

        net_impact = (
            reported_revenue
            - expected_revenue
        )

        gross_discrepancy = sum(
            abs(
                float(
                    v.get(
                        "difference",
                        0,
                    )
                )
            )
            for v in violations
        )


        st.subheader(
            "Financial Impact"
        )

        f1, f2, f3 = st.columns(3)

        f1.metric(
            "EXPECTED REVENUE",
            f"${expected_revenue:,.2f}",
        )

        f2.metric(
            "REPORTED REVENUE",
            f"${reported_revenue:,.2f}",
        )

        f3.metric(
            "NET REVENUE IMPACT",
            f"${net_impact:,.2f}",
        )

        st.caption(
            f"Gross discrepancy across affected orders: "
            f"${gross_discrepancy:,.2f}"
        )


    # =====================================================
    # ROOT CAUSE ANALYSIS
    # =====================================================

    diagnosis = result.get(
        "diagnosis",
        "",
    )

    if diagnosis:

        st.subheader(
            "Root Cause Analysis"
        )

        st.markdown(
            diagnosis
        )


    # =====================================================
    # EVALUATION
    # =====================================================

    st.subheader(
        "Evaluation"
    )

    ec1, ec2 = st.columns(2)

    ec1.metric(
        "Evaluation",
        evaluation.get(
            "status",
            "-"
        ).upper(),
    )

    ec2.metric(
        "Evidence Score",
        evaluation.get(
            "score",
            "-"
        ),
    )

    reason = evaluation.get(
        "reason",
        "",
    )

    if reason:

        st.info(
            reason
        )


    # =====================================================
    # INCIDENT REPORT
    # =====================================================

    st.subheader(
        "Incident Report"
    )

    try:

        # generate_report returns the actual Markdown text
        report_content = generate_report(
            result
        )


        # Preview
        with st.expander(
            "Preview Report"
        ):

            st.markdown(
                report_content
            )


        # Download
        st.download_button(
            label="⬇️ Download Incident Report",
            data=report_content,
            file_name="dataforge_incident_report.md",
            mime="text/markdown",
            use_container_width=True,
        )


        st.success(
            "Incident report generated successfully."
        )


    except Exception as e:

        st.error(
            f"Report generation failed: {e}"
        )