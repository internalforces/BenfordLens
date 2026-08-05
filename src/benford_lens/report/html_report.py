"""HTML report rendering (stdlib templating only — no new dependency).

Report wording follows AGENTS.md's Product Philosophy & Tone Rules: neutral
and exploratory, never accusatory or conclusive about data manipulation.
"""

from __future__ import annotations

import base64
import html
import io
import string
from dataclasses import dataclass
from datetime import datetime

from matplotlib.figure import Figure

from benford_lens.analysis.benford import BenfordResult
from benford_lens.analysis.preprocessing import PreprocessingOptions, PreprocessingPreview
from benford_lens.analysis.suitability import SuitabilityAssessment, SuitabilityLevel

_LEVEL_BADGE = {
    SuitabilityLevel.GOOD: "\U0001f7e2 Good",
    SuitabilityLevel.CAUTION: "\U0001f7e1 Caution",
    SuitabilityLevel.DIFFICULT: "\U0001f534 Difficult to determine",
}

_TEMPLATE = string.Template(
    """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Benford Lens Report — $column_name</title>
<style>
body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; color: #222; }
h1, h2 { color: #333; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }
.badge { font-weight: bold; }
footer { margin-top: 2rem; font-size: 0.85rem; color: #666; }
</style>
</head>
<body>
<h1>Benford Lens Report</h1>
<p>Source: $source_name — Column: $column_name</p>
<p>Generated: $generated_at</p>

<h2>Preprocessing</h2>
<p>$preprocessing_summary</p>

<h2>Data suitability</h2>
<p class="badge">$suitability_badge</p>
<ul>$suitability_notes</ul>

<h2>First-digit distribution</h2>
<img src="data:image/png;base64,$chart_base64" alt="Expected vs. actual first-digit distribution">
<p>$result_summary</p>
<table>
<tr><th>Digit</th><th>Observed %</th><th>Expected %</th></tr>
$digit_table_rows
</table>

<footer>
<p>This report was generated entirely on your local machine; no data was sent anywhere.</p>
<p>This result alone cannot be used to judge data errors or manipulation; further review may
be warranted.</p>
</footer>
</body>
</html>
"""
)


@dataclass
class ReportContext:
    source_name: str
    column_name: object
    preprocessing_options: PreprocessingOptions
    preprocessing_preview: PreprocessingPreview
    suitability: SuitabilityAssessment
    result: BenfordResult
    result_summary: str
    chart_figure: Figure


def _figure_to_base64(figure: Figure) -> str:
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _preprocessing_summary(options: PreprocessingOptions, preview: PreprocessingPreview) -> str:
    return (
        f"Negative values: {options.negative_handling}; zero values: {options.zero_handling}; "
        f"decimals: {options.decimal_handling}; blanks: {options.blank_handling}; "
        f"duplicates: {options.duplicate_handling}; "
        f"text-to-number: {'on' if options.string_to_number else 'off'}. "
        f"{preview.total_before} → {preview.total_after} values used."
    )


def _digit_table_rows(result: BenfordResult) -> str:
    rows = []
    for digit in sorted(result.expected_proportions):
        observed_pct = result.observed_proportions[digit] * 100
        expected_pct = result.expected_proportions[digit] * 100
        rows.append(
            f"<tr><td>{digit}</td><td>{observed_pct:.1f}%</td><td>{expected_pct:.1f}%</td></tr>"
        )
    return "\n".join(rows)


def render_html_report(context: ReportContext) -> str:
    notes_html = "".join(f"<li>{html.escape(note)}</li>" for note in context.suitability.notes)
    return _TEMPLATE.substitute(
        source_name=html.escape(context.source_name),
        column_name=html.escape(str(context.column_name)),
        generated_at=datetime.now().isoformat(timespec="seconds"),
        preprocessing_summary=_preprocessing_summary(
            context.preprocessing_options, context.preprocessing_preview
        ),
        suitability_badge=_LEVEL_BADGE[context.suitability.level],
        suitability_notes=notes_html,
        chart_base64=_figure_to_base64(context.chart_figure),
        result_summary=html.escape(context.result_summary),
        digit_table_rows=_digit_table_rows(context.result),
    )
