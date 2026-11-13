"""Read-only dashboard HTML components.

All values come from validated prediction frames. Functions in this module are
pure, making the HTML output straightforward to review and unit test. Model
names and other dynamic text are escaped before insertion into markup.
"""

from html import escape
from typing import Mapping

import pandas as pd

METRICS = {"Accuracy", "Precision", "Recall", "F1"}
OUTCOMES = (
    ("Correct normal", "True normal", "green"),
    ("Detected attacks", "Detected attacks", "teal"),
    ("False alarms", "False alarms", "orange"),
    ("Missed attacks", "Missed attacks", "coral"),
)


def kpi_grid_html(items: list[tuple[str, str, str]]) -> str:
    """Render four readable KPIs, including context below each value."""
    cards = []
    for label, value, caption in items:
        cards.append(
            '<div class="ui-kpi">'
            f'<div class="ui-kpi-label">{escape(label)}</div>'
            f'<div class="ui-kpi-value">{escape(value)}</div>'
            f'<div class="ui-kpi-caption">{escape(caption)}</div>'
            '</div>'
        )
    return '<div class="ui-kpi-grid">' + "".join(cards) + '</div>'


def score_chart_html(table: pd.DataFrame, metric: str) -> str:
    """A horizontal chart for categorical model scores, without fake trends."""
    if metric not in METRICS:
        raise ValueError("Unsupported comparison metric")
    if table.empty:
        return '<p class="ui-muted">No models are available.</p>'

    rows = []
    ordered = table.sort_values([metric, "Model"], ascending=[False, True])
    top_score = float(ordered[metric].max())
    for _, item in ordered.iterrows():
        value = float(item[metric]) * 100.0
        name = escape(str(item["Model"]))
        leader = abs(value - top_score * 100.0) < 1e-8
        rows.append(
            '<div class="ui-bar-row">'
            f'<div class="ui-bar-name">{name}</div>'
            '<div class="ui-bar-line">'
            f'<div class="ui-bar-track" role="progressbar" aria-label="{name}: {metric}" '
            f'aria-valuemin="0" aria-valuemax="100" aria-valuenow="{value:.1f}">'
            f'<div class="ui-bar-fill {"ui-bar-best" if leader else ""}" style="width:{value:.3f}%"></div>'
            '</div></div>'
            f'<div class="ui-bar-value">{value:.1f}%</div>'
            '</div>'
        )
    return (
        '<div class="ui-panel ui-bar-panel">'
        '<div class="ui-plot-axis"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>'
        + "".join(rows)
        + '<p class="ui-footnote">Higher is better for these four scores. Exact values appear in the full results table.</p>'
        '</div>'
    )


def outcome_overview_html(stats: Mapping, model_name: str) -> str:
    """Summary and accessible donut chart, modeled on a compact analytics panel."""
    counts = [int(stats[key]) for _, key, _ in OUTCOMES]
    total = sum(counts)
    proportions = [count / total * 100 if total else 0 for count in counts]
    palette = ["var(--ui-green)", "var(--ui-teal)", "var(--ui-orange)", "var(--ui-coral)"]

    segments = []
    position = 0.0
    for color, share in zip(palette, proportions):
        segments.append(f"{color} {position:.4f}% {position+share:.4f}%")
        position += share
    donut_style = escape("conic-gradient(" + ", ".join(segments) + ")", quote=True)
    label = escape(model_name)
    legend = "".join(
        '<div class="ui-legend-row">'
        f'<span class="ui-swatch ui-{name}"></span>'
        f'<span class="ui-legend-name">{escape(title)}</span>'
        f'<strong>{count:,}</strong><span class="ui-legend-rate">{share:.1f}%</span>'
        '</div>'
        for (title, _, name), count, share in zip(OUTCOMES, counts, proportions)
    )
    segments_html = "".join(
        f'<span class="ui-segment ui-{name}" style="width:{share:.4f}%" '
        f'title="{escape(title)}: {count:,}"></span>'
        for (title, _, name), count, share in zip(OUTCOMES, counts, proportions)
    )
    return (
        '<div class="ui-panel ui-outcome-panel">'
        '<div class="ui-panel-heading"><div><h3>Classification outcomes</h3>'
        f'<p>How {label} classified the available test records.</p></div></div>'
        '<div class="ui-outcome-grid">'
        '<div class="ui-outcome-left">'
        '<p class="ui-overline">Total evaluated records</p>'
        f'<div class="ui-large-number">{total:,}</div>'
        '<div class="ui-segmented" role="img" aria-label="Share of correct normal, detected attacks, false alarms, and missed attacks">'
        + segments_html + '</div>'
        '<p class="ui-soft-label">Every segment represents a distinct prediction outcome.</p>'
        '<div class="ui-mini-stats">'
        f'<div><strong>{int(stats["Detected attacks"]):,}</strong><span>Attacks detected</span></div>'
        f'<div><strong>{int(stats["Missed attacks"]):,}</strong><span>Attacks missed</span></div>'
        '</div></div>'
        '<div class="ui-outcome-right">'
        '<p class="ui-overline">Outcome distribution</p>'
        '<div class="ui-donut-content">'
        f'<div class="ui-donut" style="background:{donut_style}" role="img" '
        f'aria-label="{escape("; ".join(f"{title}: {count}" for (title, _, _), count in zip(OUTCOMES, counts)))}">'
        f'<div class="ui-donut-hole"><strong>{total:,}</strong><span>records</span></div></div>'
        '<div class="ui-legend">' + legend + '</div></div></div>'
        '</div></div>'
    )


def matrix_chart_html(stats: Mapping) -> str:
    """Semantic confusion matrix with both counts and row-based rates."""
    tn, fp, fn, tp = (int(stats[key]) for key in (
        "True normal", "False alarms", "Missed attacks", "Detected attacks"))

    def cell(value: int, label: str, denominator: int, status: str) -> str:
        rate = 100.0 * value / denominator if denominator else 0.0
        return (
            f'<td class="ui-matrix-cell ui-matrix-{status}">'
            f'<strong>{value:,}</strong><span>{escape(label)}</span>'
            f'<small>{rate:.1f}% of row</small></td>'
        )

    return (
        '<div class="ui-panel ui-matrix-panel">'
        '<div class="ui-panel-heading"><div><h3>Confusion matrix</h3>'
        '<p>Actual classification versus the model prediction.</p></div></div>'
        '<div class="ui-table-overflow">'
        '<table class="ui-matrix" aria-label="Confusion matrix comparing actual and predicted network labels">'
        '<thead><tr><th scope="col">Actual / Predicted</th>'
        '<th scope="col">Normal</th><th scope="col">Attack</th></tr></thead>'
        '<tbody><tr><th scope="row">Normal</th>'
        + cell(tn, "Correct normal", tn + fp, "good")
        + cell(fp, "False alarms", tn + fp, "bad")
        + '</tr><tr><th scope="row">Attack</th>'
        + cell(fn, "Missed attacks", fn + tp, "bad")
        + cell(tp, "Detected attacks", fn + tp, "good")
        + '</tr></tbody></table></div>'
        '<p class="ui-footnote">Rows are actual labels; columns are predictions. Values are record counts.</p>'
        '</div>'
    )


def comparison_table_html(table: pd.DataFrame) -> str:
    """Build a clean semantic table with no decorative cell grid lines."""
    columns = ("Model", "Accuracy", "Precision", "Recall", "F1", "False alarms", "Missed attacks")
    headings = "".join(
        f'<th scope="col">{escape("F1-score" if col == "F1" else col)}</th>'
        for col in columns
    )
    rows = []
    leading_f1 = table["F1"].max() if not table.empty else None
    for _, record in table.iterrows():
        model = escape(str(record["Model"]))
        is_top = float(record["F1"]) == leading_f1
        label = '<span class="ui-top-label">Top F1</span>' if is_top else ''
        cells = [f'<th scope="row"><span class="ui-model-name">{model}</span>{label}</th>']
        for column in ("Accuracy", "Precision", "Recall", "F1"):
            emphasis = ' class="ui-strong-score"' if column == "F1" else ''
            cells.append(f'<td{emphasis}>{float(record[column]):.1%}</td>')
        cells.extend(
            f'<td>{int(record[column]):,}</td>'
            for column in ("False alarms", "Missed attacks")
        )
        rows.append('<tr>' + "".join(cells) + '</tr>')
    return (
        '<div class="ui-table-overflow" role="region" '
        'aria-label="Model comparison table" tabindex="0">'
        '<table class="ui-data-table"><thead><tr>' + headings + '</tr></thead><tbody>'
        + "".join(rows) + '</tbody></table></div>'
    )


def prediction_table_html(records: pd.DataFrame) -> str:
    """Render a small prediction preview with the application's theme tokens.

    Streamlit's native dataframe grid has an independent canvas theme, so a
    semantic HTML table gives the 20-row preview consistent light/dark colors.
    Data values are escaped before being inserted into markup.
    """
    columns = ("row_id", "Actual", "Predicted", "Outcome")
    if any(column not in records.columns for column in columns):
        raise ValueError("Prediction preview is missing required columns")

    headings = "".join(f'<th scope="col">{escape(name)}</th>' for name in columns)
    rows = []
    for row_id, actual, predicted, outcome in records.loc[:, columns].itertuples(index=False, name=None):
        status = ("ui-prediction-error" if outcome in ("Missed attack", "False alarm")
                  else "")
        rows.append(
            f'<tr class="{status}">'
            f'<th scope="row">{escape(str(row_id))}</th>'
            f'<td>{escape(str(actual))}</td>'
            f'<td>{escape(str(predicted))}</td>'
            f'<td>{escape(str(outcome))}</td>'
            '</tr>'
        )

    if not rows:
        return '<p class="ui-muted">No predictions match this filter.</p>'

    return (
        '<div class="ui-table-overflow" role="region" '
        'aria-label="Prediction records" tabindex="0">'
        '<table class="ui-data-table ui-prediction-table">'
        '<thead><tr>' + headings + '</tr></thead><tbody>'
        + "".join(rows) + '</tbody></table></div>'
    )
