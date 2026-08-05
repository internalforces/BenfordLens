"""Preprocessing options panel: one combo box per rule, plus a live preview."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from benford_lens.analysis.preprocessing import PreprocessingOptions, PreprocessingPreview

_NEGATIVE_OPTIONS = [
    ("keep", "Keep"),
    ("absolute", "Convert to absolute value"),
    ("exclude", "Exclude"),
]
_ZERO_OPTIONS = [("keep", "Keep"), ("exclude", "Exclude")]
_DECIMAL_OPTIONS = [("as_is", "Use as-is"), ("round", "Round"), ("truncate", "Truncate")]
_BLANK_OPTIONS = [("exclude", "Exclude")]
_DUPLICATE_OPTIONS = [("keep", "Keep"), ("exclude", "Exclude")]
_STRING_TO_NUMBER_OPTIONS = [("true", "Auto-convert"), ("false", "Do not convert")]


class PreprocessingPanel(QWidget):
    def __init__(
        self,
        on_preview_requested: Callable[[PreprocessingOptions], None],
        on_options_changed: Callable[[], None] | None = None,
    ) -> None:
        super().__init__()
        self._on_preview_requested = on_preview_requested
        self._on_options_changed = on_options_changed

        self.negative_combo = self._build_combo(_NEGATIVE_OPTIONS, "absolute")
        self.zero_combo = self._build_combo(_ZERO_OPTIONS, "exclude")
        self.decimal_combo = self._build_combo(_DECIMAL_OPTIONS, "as_is")
        self.blank_combo = self._build_combo(_BLANK_OPTIONS, "exclude")
        self.duplicate_combo = self._build_combo(_DUPLICATE_OPTIONS, "keep")
        self.string_to_number_combo = self._build_combo(_STRING_TO_NUMBER_OPTIONS, "true")

        # Any option change makes an already-rendered analysis stale, exactly
        # like clicking Preview does — MainWindow uses this to invalidate the
        # chart and the export button.
        for combo, _default_value in self._combos():
            combo.currentIndexChanged.connect(self._emit_options_changed)

        self.negative_label = QLabel(self.tr("Negative values"))
        self.zero_label = QLabel(self.tr("Zero values"))
        self.decimal_label = QLabel(self.tr("Decimal values"))
        self.blank_label = QLabel(self.tr("Blank values"))
        self.duplicate_label = QLabel(self.tr("Duplicate values"))
        self.string_to_number_label = QLabel(self.tr("Text-to-number"))

        self.preview_button = QPushButton(self.tr("Preview"))
        self.preview_button.clicked.connect(self._on_preview_clicked)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        form = QFormLayout()
        form.addRow(self.negative_label, self.negative_combo)
        form.addRow(self.zero_label, self.zero_combo)
        form.addRow(self.decimal_label, self.decimal_combo)
        form.addRow(self.blank_label, self.blank_combo)
        form.addRow(self.duplicate_label, self.duplicate_combo)
        form.addRow(self.string_to_number_label, self.string_to_number_combo)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.preview_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def _build_combo(self, options: list[tuple[str, str]], default_value: str) -> QComboBox:
        combo = QComboBox()
        for value, label in options:
            combo.addItem(self.tr(label), value)
        combo.setCurrentIndex(max(combo.findData(default_value), 0))
        return combo

    def _combos(self) -> list[tuple[QComboBox, str]]:
        """Every option combo paired with its documented default value."""
        return [
            (self.negative_combo, "absolute"),
            (self.zero_combo, "exclude"),
            (self.decimal_combo, "as_is"),
            (self.blank_combo, "exclude"),
            (self.duplicate_combo, "keep"),
            (self.string_to_number_combo, "true"),
        ]

    def _emit_options_changed(self) -> None:
        if self._on_options_changed is not None:
            self._on_options_changed()

    def reset_to_defaults(self) -> None:
        """Restore every combo to the PreprocessingOptions dataclass defaults.

        Called when a new file is loaded, where SessionController resets
        `state.preprocessing_options` — without this the panel would keep
        showing the previous file's selections while the controller computed
        against the defaults.
        """
        for combo, default_value in self._combos():
            # Blocked so this bookkeeping reset does not fire the
            # options-changed callback; the caller is already invalidating.
            was_blocked = combo.blockSignals(True)
            combo.setCurrentIndex(max(combo.findData(default_value), 0))
            combo.blockSignals(was_blocked)
        # The preview line describes the previous file's column; drop it too.
        self.result_label.setText("")

    def retranslate_ui(self) -> None:
        self.negative_label.setText(self.tr("Negative values"))
        self.zero_label.setText(self.tr("Zero values"))
        self.decimal_label.setText(self.tr("Decimal values"))
        self.blank_label.setText(self.tr("Blank values"))
        self.duplicate_label.setText(self.tr("Duplicate values"))
        self.string_to_number_label.setText(self.tr("Text-to-number"))
        self.preview_button.setText(self.tr("Preview"))
        self._retranslate_combo(self.negative_combo, _NEGATIVE_OPTIONS)
        self._retranslate_combo(self.zero_combo, _ZERO_OPTIONS)
        self._retranslate_combo(self.decimal_combo, _DECIMAL_OPTIONS)
        self._retranslate_combo(self.blank_combo, _BLANK_OPTIONS)
        self._retranslate_combo(self.duplicate_combo, _DUPLICATE_OPTIONS)
        self._retranslate_combo(self.string_to_number_combo, _STRING_TO_NUMBER_OPTIONS)

    def _retranslate_combo(self, combo: QComboBox, options: list[tuple[str, str]]) -> None:
        for index, (_value, label) in enumerate(options):
            combo.setItemText(index, self.tr(label))

    def current_options(self) -> PreprocessingOptions:
        return PreprocessingOptions(
            negative_handling=self.negative_combo.currentData(),
            zero_handling=self.zero_combo.currentData(),
            decimal_handling=self.decimal_combo.currentData(),
            blank_handling=self.blank_combo.currentData(),
            duplicate_handling=self.duplicate_combo.currentData(),
            string_to_number=self.string_to_number_combo.currentData() == "true",
        )

    def _on_preview_clicked(self) -> None:
        self._on_preview_requested(self.current_options())

    def show_preview(self, preview: PreprocessingPreview) -> None:
        self.result_label.setText(
            f"{preview.total_before} → {preview.total_after} "
            + self.tr(
                "values (excluded: {blank} blank, {non_numeric} non-numeric, "
                "{negative} negative, {zero} zero)"
            ).format(
                blank=preview.excluded_blank,
                non_numeric=preview.excluded_non_numeric,
                negative=preview.excluded_negative,
                zero=preview.excluded_zero,
            )
            + f"\n{self.tr('Before')}: {preview.sample_before}"
            + f"\n{self.tr('After')}: {preview.sample_after}"
        )
