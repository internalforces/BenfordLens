"""Generate portfolio screenshots and a short GIF from deterministic synthetic data.

The script opens the real PySide6 application in Qt's offscreen mode. It never reads user data
and writes only the generated visual assets under ``docs/assets``.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
from PIL import Image
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from benford_lens.analysis.benford import DigitPosition  # noqa: E402
from benford_lens.ui.controller import AnalysisMode  # noqa: E402
from benford_lens.ui.main_window import MainWindow  # noqa: E402

OUTPUT_DIR = ROOT / "docs" / "assets"
WINDOW_SIZE = (1440, 960)
GIF_WIDTH = 960


def build_synthetic_dataset() -> pd.DataFrame:
    """Return a deterministic, fictional transaction-style dataset."""
    rng = np.random.default_rng(20260809)
    raw_amounts = 10 ** rng.uniform(1.0, 6.2, 640)
    departments = np.array(["Operations", "Sales", "Research", "Support"])
    amount_values: list[object] = []
    for index, amount in enumerate(raw_amounts):
        rounded = round(float(amount), 2)
        if index % 97 == 0:
            amount_values.append(None)
        elif index % 71 == 0:
            amount_values.append(0)
        elif index % 43 == 0:
            amount_values.append(f"${rounded:,.2f}")
        elif index % 37 == 0:
            amount_values.append(-rounded)
        else:
            amount_values.append(rounded)

    return pd.DataFrame(
        {
            "record_id": [f"SYN-{index + 1:04d}" for index in range(len(raw_amounts))],
            "department": departments[np.arange(len(raw_amounts)) % len(departments)],
            "amount": amount_values,
            "invoice_date": pd.date_range("2025-01-01", periods=len(raw_amounts), freq="D"),
        }
    )


def settle(application: QApplication, milliseconds: int = 140) -> None:
    """Let Qt layouts and Matplotlib canvases finish painting."""
    application.processEvents()
    QTest.qWait(milliseconds)
    application.processEvents()


def capture(window: MainWindow, path: Path) -> Path:
    """Capture the actual application window to a PNG."""
    path.parent.mkdir(parents=True, exist_ok=True)
    pixmap = window.grab()
    if not pixmap.save(str(path), "PNG"):
        raise RuntimeError(f"Could not save screenshot: {path}")
    return path


def build_gif(frame_paths: list[Path], output_path: Path) -> None:
    """Encode captured screenshots into a compact, looping workflow GIF."""
    frames: list[Image.Image] = []
    for frame_path in frame_paths:
        with Image.open(frame_path) as image:
            height = round(image.height * GIF_WIDTH / image.width)
            resized = image.convert("RGB").resize((GIF_WIDTH, height), Image.Resampling.LANCZOS)
            frames.append(resized.quantize(colors=128, method=Image.Quantize.MEDIANCUT))

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=[1300, 1500, 1700, 1700, 2000],
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    application = QApplication.instance() or QApplication([])
    assert isinstance(application, QApplication)

    with tempfile.TemporaryDirectory(prefix="benford-lens-portfolio-") as temp_dir:
        temp_root = Path(temp_dir)
        synthetic_path = temp_root / "synthetic_transactions.csv"
        build_synthetic_dataset().to_csv(synthetic_path, index=False)

        window = MainWindow()
        window.resize(*WINDOW_SIZE)
        window.show()
        settle(application)

        window.load_file(str(synthetic_path))
        amount_row = next(
            row
            for row in range(window.column_table.rowCount())
            if window.column_table.item(row, 0).text() == "amount"
        )
        window.column_table.selectRow(amount_row)
        window.scroll_area.verticalScrollBar().setValue(0)
        settle(application)

        frame_paths: list[Path] = []
        frame_paths.append(capture(window, temp_root / "01-column-selected.png"))

        window._on_preprocessing_preview_requested(window.preprocessing_panel.current_options())
        window.scroll_area.ensureWidgetVisible(window.preprocessing_panel, 0, 20)
        settle(application)
        frame_paths.append(capture(window, temp_root / "02-preview.png"))

        window.mode_combo.setCurrentIndex(window.mode_combo.findData(AnalysisMode.COMBINED.value))
        window._on_analyze_clicked()
        window.scroll_area.ensureWidgetVisible(window.results_widget, 0, 20)
        settle(application, 240)
        overview_en = capture(window, OUTPUT_DIR / "benford-lens-overview-en.png")
        frame_paths.append(overview_en)

        window.expert_statistics_panel.toggle_button.setChecked(True)
        window.scroll_area.ensureWidgetVisible(window.expert_statistics_panel, 0, 20)
        settle(application)
        frame_paths.append(capture(window, temp_root / "04-expert-details.png"))

        window.first_result_panel.digit_clicked.emit(DigitPosition.FIRST, 1)
        window.scroll_area.ensureWidgetVisible(window.drill_down_panel, 0, 20)
        settle(application)
        frame_paths.append(capture(window, temp_root / "05-drill-down.png"))

        window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))
        snapshot = window.controller.state.analysis_snapshot
        assert snapshot is not None
        window.preprocessing_panel.show_preview(snapshot.preprocessing_preview)
        window.expert_statistics_panel.toggle_button.setChecked(False)
        window.scroll_area.ensureWidgetVisible(window.results_widget, 0, 20)
        settle(application, 240)
        capture(window, OUTPUT_DIR / "benford-lens-overview-ko.png")

        window.first_result_panel.digit_clicked.emit(DigitPosition.FIRST, 1)
        window.scroll_area.ensureWidgetVisible(window.drill_down_panel, 0, 20)
        settle(application)
        capture(window, OUTPUT_DIR / "benford-lens-drilldown-ko.png")

        build_gif(frame_paths, OUTPUT_DIR / "benford-lens-workflow.gif")
        window.close()


if __name__ == "__main__":
    main()
