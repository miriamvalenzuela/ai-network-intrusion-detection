"""Data-grounded explanations for the model comparison.

All observations are derived from the currently loaded prediction files.
No conclusions about live network performance are made from test scores.
"""

from html import escape

import pandas as pd


def _item(title: str, value: str, explanation: str) -> str:
    """Format one self-contained finding with accessible text hierarchy."""
    return (
        '<div class="ui-finding">'
        f'<div class="ui-finding-label">{escape(title)}</div>'
        f'<strong>{escape(value)}</strong>'
        f'<p>{escape(explanation)}</p>'
        '</div>'
    )


def insights_html(table: pd.DataFrame, *, demo: bool) -> str:
    """Explain performance and error trade-offs for the available models.

    The table comes from ``dashboard_data.comparison_table`` and has one row
    per model. Models use identical ground-truth labels and test-row order.
    """
    if table.empty:
        return '<p class="ui-muted">Add a valid results file to see model insights.</p>'

    leading_f1 = table.sort_values(["F1", "Recall", "Model"], ascending=[False, False, True]).iloc[0]
    leading_recall = table.sort_values(["Recall", "F1", "Model"], ascending=[False, False, True]).iloc[0]
    fewest_alarms = table.sort_values(["False alarms", "Missed attacks", "Model"]).iloc[0]

    attacks = int(table.iloc[0]["Detected attacks"] + table.iloc[0]["Missed attacks"])
    normal = int(table.iloc[0]["True normal"] + table.iloc[0]["False alarms"])
    total = attacks + normal
    attack_share = attacks / total if total else 0.0
    recall_misses = int(leading_recall["Missed attacks"])
    recall_false_alarms = int(leading_recall["False alarms"])
    alarm_rate = recall_false_alarms / normal if normal else 0.0
    best_f1 = float(leading_f1["F1"])

    if len(table) > 1:
        runner_up = table.sort_values(["F1", "Recall", "Model"], ascending=[False, False, True]).iloc[1]
        f1_margin = (best_f1 - float(runner_up["F1"])) * 100.0
        best_explanation = (
            f"The F1-score is {f1_margin:.1f} percentage points higher than "
            f"{runner_up['Model']} ({float(runner_up['F1']):.1%}). "
            "This compares precision and recall on the loaded test records."
        )
    else:
        best_explanation = (
            "Only one model is available, so there is not yet a meaningful "
            "cross-model ranking."
        )

    primary = [
        _item(
            "Best precision / recall balance",
            f"{leading_f1['Model']}  ·  {best_f1:.1%} F1",
            best_explanation,
        ),
        _item(
            "Attack detection trade-off",
            f"{leading_recall['Model']}  ·  {float(leading_recall['Recall']):.1%} recall",
            f"It missed {recall_misses:,} of {attacks:,} labeled attacks, "
            f"but also flagged {recall_false_alarms:,} normal records "
            f"({alarm_rate:.1%} false alarm rate).",
        ),
        _item(
            "False-alarm comparison",
            f"{fewest_alarms['Model']}  ·  {int(fewest_alarms['False alarms']):,} false alarms",
            f"This model missed {int(fewest_alarms['Missed attacks']):,} attacks. "
            "Fewer alerts do not necessarily mean better attack coverage.",
        ),
    ]

    mode_note = (
        "These files are fabricated examples. The rankings and differences "
        "demonstrate how the dashboard works, not how the algorithms perform "
        "on the UNSW-NB15 test set."
        if demo else
        "These comparisons describe the held-out UNSW-NB15 test set only. "
        "Results are not evidence of real-time deployment performance."
    )

    return (
        '<div class="ui-insight-grid">'
        '<section class="ui-insight-panel" aria-label="Evidence from current model results">'
        '<div class="ui-insight-heading"><h3>Performance highlights</h3>'
        '<p>Rankings and error counts calculated from the current CSV files.</p></div>'
        + ''.join(primary)
        + '</section>'
        '<section class="ui-insight-panel" aria-label="Interpretation and limitations">'
        '<div class="ui-insight-heading"><h3>What to consider</h3>'
        '<p>Putting these scores into context.</p></div>'
        '<div class="ui-context-stat">'
        f'<strong>{attacks:,} of {total:,}</strong>'
        '<span>labeled attack records</span>'
        f'<p>Attacks make up {attack_share:.1%} of this test set. '
        'Accuracy alone can hide missed attacks, especially when classes are uneven.</p>'
        '</div>'
        '<div class="ui-context-block"><strong>Recall versus false alarms</strong>'
        '<p>Higher recall means fewer attacks go undetected. However, '
        'flagging more traffic as suspicious can increase the burden on analysts. '
        'Look at missed attacks and false alarms together.</p></div>'
        '<div class="ui-context-block"><strong>Scope of the conclusion</strong>'
        f'<p>{escape(mode_note)}</p></div>'
        '</section></div>'
    )
