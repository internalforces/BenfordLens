"""Suitability panel: an advisory 🟢/🟡/🔴 signal plus the underlying notes.

Never states or implies whether Benford's Law applies to the data — see
AGENTS.md's Product Philosophy & Tone Rules.
"""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from benford_lens.analysis.suitability import SuitabilityAssessment, SuitabilityLevel


class SuitabilityPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.badge_label = QLabel("")
        self.notes_label = QLabel("")
        self.notes_label.setWordWrap(True)
        self.caption_label = QLabel(self._caption_text())
        self.caption_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.badge_label)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.caption_label)
        self.setLayout(layout)

    def _caption_text(self) -> str:
        return self.tr(
            "These are data characteristics, not a determination of whether Benford's Law "
            "applies — that judgment is yours to make."
        )

    def _badge_text(self, level: SuitabilityLevel) -> str:
        if level is SuitabilityLevel.GOOD:
            return self.tr("\U0001f7e2 Good")
        if level is SuitabilityLevel.CAUTION:
            return self.tr("\U0001f7e1 Caution")
        return self.tr("\U0001f534 Difficult to determine")

    def show_assessment(self, assessment: SuitabilityAssessment) -> None:
        self.badge_label.setText(self._badge_text(assessment.level))
        notes_text = "\n".join(f"• {note}" for note in assessment.notes)
        self.notes_label.setText(notes_text or self.tr("No caveats found."))

    def clear(self) -> None:
        """Blank the badge and notes.

        Called when a new file is loaded: the previous file's badge would
        otherwise stay on screen describing data that is no longer open.
        """
        self.badge_label.setText("")
        self.notes_label.setText("")

    def retranslate_ui(self) -> None:
        self.caption_label.setText(self._caption_text())
