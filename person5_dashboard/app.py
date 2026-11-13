"""Streamlit interface for the team's offline network intrusion study.

Run from the repository root:
    streamlit run person5_dashboard/app.py

This application evaluates existing predictions. It never trains models, reads
live network traffic, or modifies classmates' result files.
"""

from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard_charts import (
    comparison_table_html,
    kpi_grid_html,
    matrix_chart_html,
    outcome_overview_html,
    score_chart_html,
)
from dashboard_controls import menu_select
from dashboard_data import (
    MODEL_NAMES,
    OFFICIAL_TEST_ROWS,
    comparison_table,
    load_results,
    model_statistics,
)
from dashboard_theme import build_theme_css

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIRECTORY = Path(__file__).resolve().parent
DEMO_DIRECTORY = APP_DIRECTORY / "demo"
RESULTS_DIRECTORY = PROJECT_ROOT / "results"

st.set_page_config(
    page_title="AI Network Intrusion Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def html(markup: str) -> None:
    """Render trusted markup generated locally by dashboard components."""
    st.markdown(markup, unsafe_allow_html=True)


def heading(title: str, description: str) -> None:
    html(
        '<div class="ui-section">'
        f'<div><h2>{escape(title)}</h2><p>{escape(description)}</p></div>'
        '</div>'
    )


def render_sidebar() -> tuple[str, bool, str]:
    """Place navigation, data selection, and appearance in one predictable area."""
    with st.sidebar:
        html(
            '<div class="ui-brand"><div class="ui-brand-mark" aria-hidden="true">NI</div>'
            '<div><div class="ui-brand-name">Network Insights</div>'
            '<div class="ui-brand-tagline">AI model evaluation</div></div></div>'
        )
        html('<div class="ui-sidebar-head">Workspace</div>')
        page = st.radio(
            "Navigate",
            ["Overview", "Model details", "How it works"],
            label_visibility="collapsed",
            key="navigation",
        )
        html('<div class="ui-sidebar-head">Data</div>')
        source = menu_select(
            "Prediction source",
            ["Guided demo", "Team results"],
            help_text="Guided demo uses synthetic predictions. Team results reads validated files from results/.",
            key="prediction_source",
        )
        st.caption("Demo results are illustrative. Use Team results for your group's real evaluation.")
        html('<div class="ui-sidebar-head">Appearance</div>')
        dark_mode = st.toggle("Dark mode", key="dark_mode", value=False)
        html(
            '<div class="ui-sidebar-foot"><strong>About this workspace</strong><br>'
            'Compare four classification methods on saved UNSW-NB15 predictions. '
            'This is a research dashboard, not a live network monitor.</div>'
        )
    theme = "Dark" if dark_mode else "Light"
    return page, source == "Team results", theme


def render_page_header(title: str, subtitle: str, real_mode: bool) -> None:
    label = "TEAM RESULTS" if real_mode else "GUIDED DEMO"
    html(
        '<div class="ui-header"><div>'
        '<div class="ui-eyebrow">AI RESEARCH / NETWORK SECURITY</div>'
        f'<h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>'
        '<div class="ui-tag"><span class="ui-tag-dot"></span>'
        f'{label}</div></div>'
    )
    if not real_mode:
        html(
            '<div class="ui-notice"><strong>Demo data</strong> · These are small, fabricated '
            'practice predictions. Scores shown here are not findings from the research dataset.</div>'
        )
    else:
        html(
            '<div class="ui-notice"><strong>Official test results</strong> · Only fully validated '
            'prediction files are included in the comparison.</div>'
        )


@st.cache_data(show_spinner=False)
def cached_results(directory: str, signature: tuple, real: bool):
    """Reload CSVs when the available files change on disk."""
    return load_results(Path(directory), real=real)


def file_signature(directory: Path) -> tuple:
    if not directory.exists():
        return ()
    return tuple(
        (path.name, path.stat().st_size, path.stat().st_mtime_ns)
        for path in sorted(directory.glob("p[1-4].csv"))
    )


def render_availability(report, real_mode: bool) -> None:
    if report.problems:
        with st.expander(f"Files requiring attention ({len(report.problems)})", expanded=True):
            for message in report.problems:
                st.error(message)
            st.caption("Invalid files are omitted. Ask the model owner to correct their export.")
    if real_mode and report.missing:
        st.info(f"Awaiting {len(report.missing)} model(s): {', '.join(report.missing)}. Available files can still be reviewed.")


def render_overview(frames: dict[int, pd.DataFrame]) -> None:
    if not frames:
        st.info("No valid prediction files are available. Select Guided demo or add the team's CSV files in results/.")
        return

    table = comparison_table(frames)
    best_f1 = table.loc[table["F1"].idxmax()]
    best_recall = table.loc[table["Recall"].idxmax()]

    heading("At a Glance", "A consistent view of model quality across the same labeled test records.")
    html(kpi_grid_html([
        ("Models available", f"{len(frames)} / 4", "Validated prediction files"),
        ("Records per model", f"{len(next(iter(frames.values()))):,}", "Aligned test records"),
        ("Top F1-score", f"{best_f1['F1']:.1%}", str(best_f1["Model"])),
        ("Top attack recall", f"{best_recall['Recall']:.1%}", str(best_recall["Model"])),
    ]))

    # An outcome mix is meaningful for a single model; never pool predictions
    # across models, since that would count the same test records repeatedly.
    left, right = st.columns([3, 1.3], vertical_alignment="bottom")
    with left:
        heading("Traffic Classification", "A breakdown of the decisions made by one model.")
    with right:
        chosen = menu_select(
            "Inspect outcomes for:",
            options=list(frames),
            format_func=lambda number: MODEL_NAMES[number],
            key="overview_model",
        )
    html(outcome_overview_html(model_statistics(frames[chosen]), MODEL_NAMES[chosen]))

    left, right = st.columns([3, 1.3], vertical_alignment="bottom")
    with left:
        heading("Compare the Models", "View a score across all available algorithms.")
    with right:
        metric = menu_select(
            "Score to compare:", ["Recall", "F1", "Precision", "Accuracy"],
            key="overview_metric",
            help_text="Recall: attacks detected. F1: balance of precision and recall.",
        )
    html(score_chart_html(table, metric))

    heading("Complete Results", "Exact model scores and classification errors.")
    html(comparison_table_html(table))
    st.download_button(
        "Download Comparison CSV",
        data=table.drop(columns=["Model number"]).to_csv(index=False).encode("utf-8"),
        file_name="model_comparison.csv",
        mime="text/csv",
        help="Use this file for your class report or presentation.",
    )

    heading("What the Data Tells Us", "These observations apply only to the loaded test files.")
    main, aside = st.columns([1, 1], gap="medium")
    with main:
        missed = table.loc[table["Missed attacks"].idxmin()]
        html(
            '<div class="ui-callout"><h3>Key findings</h3>'
            '<div class="ui-insight"><span>Best balanced performance</span>'
            f'<strong>{escape(str(best_f1["Model"]))} · {best_f1["F1"]:.1%} F1</strong></div>'
            '<div class="ui-insight"><span>Highest attack detection rate</span>'
            f'<strong>{escape(str(best_recall["Model"]))} · {best_recall["Recall"]:.1%} recall</strong></div>'
            '<div class="ui-insight"><span>Fewest missed attacks</span>'
            f'<strong>{escape(str(missed["Model"]))} · {int(missed["Missed attacks"]):,} missed</strong></div>'
            '</div>'
        )
    with aside:
        html(
            '<div class="ui-info-card"><h3>How to read the comparison</h3>'
            '<p><strong>Recall</strong> is especially relevant here because missed attacks '
            'may go undetected.</p><p><strong>Precision</strong> shows how often attack alerts '
            'are correct. Low precision produces more false alarms.</p>'
            '<p><strong>F1-score</strong> balances those concerns. A better test score '
            'does not guarantee performance on live networks.</p></div>'
        )


def render_model_details(frames: dict[int, pd.DataFrame]) -> None:
    if not frames:
        st.info("No valid models are available yet. Choose Guided demo to explore this page.")
        return

    chosen = menu_select(
        "Select a model:",
        list(frames),
        format_func=lambda number: MODEL_NAMES[number],
        key="detail_model",
    )
    selected = frames[chosen]
    stats = model_statistics(selected)

    heading("Performance snapshot", "Scores for the selected model, calculated from its predictions.")
    html(kpi_grid_html([
        ("Accuracy", f"{stats['Accuracy']:.1%}", "All predictions"),
        ("Precision", f"{stats['Precision']:.1%}", "Reliability of attack alerts"),
        ("Attack recall", f"{stats['Recall']:.1%}", "Share of attacks detected"),
        ("F1-score", f"{stats['F1']:.1%}", "Precision / recall balance"),
    ]))

    heading("Understanding mistakes", "The counts reveal which mistakes are hidden behind the score.")
    left, right = st.columns([1.35, 1], gap="medium")
    with left:
        html(matrix_chart_html(stats))
    with right:
        html(
            '<div class="ui-panel"><div class="ui-panel-heading"><div>'
            '<h3>Error breakdown</h3><p>How many records were classified correctly or incorrectly.</p>'
            '</div></div><div class="ui-detail-stats">'
            + "".join(
                f'<div class="ui-detail-item"><strong>{int(stats[key]):,}</strong><span>{escape(label)}</span></div>'
                for key, label in [
                    ("Missed attacks", "Missed attacks"), ("False alarms", "False alarms"),
                    ("Detected attacks", "Detected attacks"), ("True normal", "Correct normal"),
                ]
            )
            + '</div><p class="ui-footnote">False alarm rate: '
            f'{stats["False alarm rate"]:.1%} of actual normal records.</p></div>'
        )

    heading("Inspect predictions", "Filter individual records without changing the stored model output.")
    condition = menu_select(
        "Filter records",
        ["All records", "Missed attacks", "False alarms", "Correct predictions"],
        key="prediction_filter",
    )
    rows = selected.copy()
    missed_mask = (rows["y_true"] == 1) & (rows["y_pred"] == 0)
    alarms_mask = (rows["y_true"] == 0) & (rows["y_pred"] == 1)
    rows["Actual"] = rows["y_true"].map({0: "Normal", 1: "Attack"})
    rows["Predicted"] = rows["y_pred"].map({0: "Normal", 1: "Attack"})
    rows["Outcome"] = "Correct"
    rows.loc[missed_mask, "Outcome"] = "Missed attack"
    rows.loc[alarms_mask, "Outcome"] = "False alarm"
    if condition == "Missed attacks":
        rows = rows.loc[missed_mask]
    elif condition == "False alarms":
        rows = rows.loc[alarms_mask]
    elif condition == "Correct predictions":
        rows = rows.loc[~(missed_mask | alarms_mask)]

    display_columns = ["row_id", "Actual", "Predicted", "Outcome"]
    st.caption(f"Showing 20 of {len(rows):,} matching rows; original row IDs are preserved.")
    st.dataframe(rows[display_columns].head(20), use_container_width=True, hide_index=True)
    st.download_button(
        "Export filtered records",
        rows[display_columns].to_csv(index=False).encode("utf-8"),
        file_name=f"p{chosen}_filtered_predictions.csv", mime="text/csv",
    )
    st.caption("An attack prediction is a classification label, not proof of a current real-world incident.")


def render_guide() -> None:
    heading("Get oriented in three steps", "No machine-learning background is required to explore this dashboard.")
    steps = [
        ("Choose your data", "Guided demo uses small practice examples. Team results uses real exported predictions from your classmates."),
        ("Compare model scores", "Open Overview to compare recall, F1, precision, and accuracy. Every score comes from prediction CSVs."),
        ("Investigate mistakes", "Open Model details to see the confusion matrix and review false alarms or missed attacks."),
    ]
    html(
        '<div class="ui-panel ui-guide-list">'
        + "".join(
            f'<div class="ui-guide-item"><div class="ui-guide-number">{index}</div>'
            f'<div><strong>{escape(title)}</strong><p>{escape(description)}</p></div></div>'
            for index, (title, description) in enumerate(steps, 1)
        ) + '</div>'
    )
    heading("Metric glossary", "A few terms you will see throughout the application.")
    glossary = [
        ("Accuracy", "Percentage of all test records that the model classified correctly."),
        ("Precision", "When a model flags a record as an attack, how often it is correct."),
        ("Recall", "Percentage of actual attacks the model detects."),
        ("F1-score", "One number balancing precision and recall."),
        ("False alarm", "Normal traffic incorrectly flagged as an attack."),
        ("Missed attack", "An attack incorrectly classified as normal traffic."),
    ]
    html(
        '<div class="ui-panel">'
        + "".join(
            f'<div class="ui-definition"><strong>{escape(term)}</strong>'
            f'<span>{escape(description)}</span></div>'
            for term, description in glossary
        ) + '</div>'
    )
    heading("The four approaches", "Each teammate uses a different machine-learning method.")
    models = [
        ("Logistic Regression", "A straightforward supervised classifier used as a baseline."),
        ("Random Forest", "Combines many decision trees to classify traffic."),
        ("Linear SVM", "Learns a boundary that separates normal and attack records."),
        ("Isolation Forest", "Learns normal patterns and flags unusual records as possible anomalies."),
    ]
    html(
        '<div class="ui-panel">'
        + "".join(
            f'<div class="ui-definition"><strong>{escape(name)}</strong>'
            f'<span>{escape(description)}</span></div>'
            for name, description in models
        ) + '</div>'
    )
    heading("Using real results", "The dashboard does not train models; it reads each person's exported CSV.")
    st.code(
        "results/p1.csv  # Logistic Regression\nresults/p2.csv  # Random Forest\n"
        "results/p3.csv  # Linear SVM\nresults/p4.csv  # Isolation Forest",
        language="text",
    )
    st.code("row_id,y_true,y_pred\n0,0,0\n1,1,1\n2,1,0", language="csv")
    st.markdown(
        f"Each real CSV must contain **{OFFICIAL_TEST_ROWS:,} rows** and match the other files' "
        "ground-truth labels. Invalid or missing model files are excluded with an explanation. "
        "This is offline research on a historical dataset, not live attack detection."
    )


def main() -> None:
    page, real_mode, theme = render_sidebar()
    html(f"<style>{build_theme_css(theme)}</style>")

    directory = RESULTS_DIRECTORY if real_mode else DEMO_DIRECTORY
    report = cached_results(str(directory), file_signature(directory), real_mode)

    titles = {
        "Overview": ("AI Network Intrusion Detection Dashboard", "Understand and compare how four AI models identify suspicious network traffic."),
        "Model details": ("Model details", "Explore prediction errors, attack detection, and individual records."),
        "How it works": ("How it works", "A short guide to the project, its models, and the metrics you will see."),
    }
    render_page_header(*titles[page], real_mode)
    render_availability(report, real_mode)

    if page == "Overview":
        render_overview(report.frames)
    elif page == "Model details":
        render_model_details(report.frames)
    else:
        render_guide()

    html('<div class="ui-footer">Network Insights / AI final project · Offline UNSW-NB15 evaluation · Built with Streamlit</div>')


if __name__ == "__main__":
    main()
