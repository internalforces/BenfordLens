"""Framework-agnostic session state and workflow orchestration.

Deliberately has no PySide6 import: MainWindow is a thin wrapper around
this controller so the workflow logic stays independently testable.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass, field, replace
from enum import Enum

import pandas as pd

from benford_lens.analysis.benford import (
    BenfordResult,
    CombinedBenfordResult,
    DigitPosition,
    analyze_combined_with_digit_pairs,
)
from benford_lens.analysis.expert_statistics import (
    CombinedExpertStatistics,
    ExpertStatistics,
    calculate_combined_expert_statistics,
    calculate_expert_statistics,
)
from benford_lens.analysis.preprocessing import (
    PreprocessingOptions,
    PreprocessingPreview,
    apply_preprocessing,
)
from benford_lens.analysis.suitability import (
    SuitabilityAssessment,
    assess_suitability,
    compute_suitability_metrics,
)
from benford_lens.io.csv_loader import load_csv
from benford_lens.io.excel_loader import list_sheets, load_excel

AnalysisResult = BenfordResult | CombinedBenfordResult
AnalysisStatistics = ExpertStatistics | CombinedExpertStatistics


class AnalysisMode(Enum):
    """User-selectable analysis modes."""

    FIRST = "first"
    SECOND = "second"
    COMBINED = "combined"


@dataclass(frozen=True)
class RowDigitMapping:
    """Original dataframe index and its normalized significant digits."""

    index: Hashable
    first: int
    second: int


@dataclass(frozen=True)
class AnalysisSnapshot:
    """All derived state produced by one explicit analysis action."""

    mode: AnalysisMode
    preprocessing_options: PreprocessingOptions
    preprocessing_preview: PreprocessingPreview
    suitability: SuitabilityAssessment
    result: AnalysisResult
    expert_statistics: AnalysisStatistics
    row_digit_mappings: tuple[RowDigitMapping, ...]


@dataclass
class SessionState:
    dataframe: pd.DataFrame | None = None
    # pandas column labels are not guaranteed to be str — pd.read_excel can
    # yield int (or other hashable) labels for numeric header cells, so this
    # must accept anything that can appear as a DataFrame column label.
    # Which worksheet the dataframe came from; None for CSV sources. The
    # exported report records it so a multi-sheet workbook stays traceable.
    sheet_name: str | None = None
    selected_column: Hashable | None = None
    preprocessing_options: PreprocessingOptions = field(default_factory=PreprocessingOptions)
    analysis_mode: AnalysisMode = AnalysisMode.FIRST
    analysis_snapshot: AnalysisSnapshot | None = None

    @property
    def last_result(self) -> AnalysisResult | None:
        """Compatibility view of the most recent snapshot result."""
        return None if self.analysis_snapshot is None else self.analysis_snapshot.result

    @property
    def last_preprocessing_options(self) -> PreprocessingOptions | None:
        """Compatibility view of the snapshotted preprocessing options."""
        return (
            None if self.analysis_snapshot is None else self.analysis_snapshot.preprocessing_options
        )

    @property
    def last_preprocessing_preview(self) -> PreprocessingPreview | None:
        """Compatibility view of the snapshotted preprocessing preview."""
        return (
            None if self.analysis_snapshot is None else self.analysis_snapshot.preprocessing_preview
        )

    @property
    def last_suitability(self) -> SuitabilityAssessment | None:
        """Compatibility view of the snapshotted suitability assessment."""
        return None if self.analysis_snapshot is None else self.analysis_snapshot.suitability

    @property
    def last_expert_statistics(self) -> AnalysisStatistics | None:
        """Compatibility view of the snapshotted reference statistics."""
        return None if self.analysis_snapshot is None else self.analysis_snapshot.expert_statistics


class SessionController:
    def __init__(self) -> None:
        self.state: SessionState = SessionState()

    def open_csv(self, path: str) -> pd.DataFrame:
        self.state = SessionState(dataframe=load_csv(path))
        return self.state.dataframe

    def list_excel_sheets(self, path: str) -> list[str]:
        return list_sheets(path)

    def open_excel(self, path: str, sheet_name: str) -> pd.DataFrame:
        self.state = SessionState(dataframe=load_excel(path, sheet_name), sheet_name=sheet_name)
        return self.state.dataframe

    def column_names(self) -> list[Hashable]:
        if self.state.dataframe is None:
            return []
        return list(self.state.dataframe.columns)

    def select_column(self, column: Hashable) -> None:
        if self.state.dataframe is None or column not in self.state.dataframe.columns:
            raise ValueError(f"Unknown column: {column}")
        if column != self.state.selected_column:
            self._invalidate_snapshot()
        self.state.selected_column = column

    def set_analysis_mode(self, mode: AnalysisMode) -> None:
        """Select an analysis mode and invalidate results from another mode."""
        if mode is not self.state.analysis_mode:
            self.state.analysis_mode = mode
            self._invalidate_snapshot()

    def analyze(self, mode: AnalysisMode | None = None) -> AnalysisResult:
        """Run the selected analysis mode from one preprocessing pass."""
        if mode is not None:
            self.set_analysis_mode(mode)
        # One preprocessing pass feeds the result, the preview and the
        # suitability metrics, so the derived snapshot cannot mix states.
        raw_series = self._raw_selected_series()
        options = self.state.preprocessing_options
        numeric_series, preview = apply_preprocessing(raw_series, options)
        assessment = assess_suitability(compute_suitability_metrics(numeric_series, raw_series))
        selected_mode = self.state.analysis_mode
        combined_result, digit_pairs = analyze_combined_with_digit_pairs(numeric_series)

        if selected_mode is AnalysisMode.FIRST:
            first_result = combined_result.first
            result: AnalysisResult = first_result
            expert_statistics: AnalysisStatistics = calculate_expert_statistics(
                numeric_series, first_result
            )
        elif selected_mode is AnalysisMode.SECOND:
            second_result = combined_result.second
            result = second_result
            expert_statistics = calculate_expert_statistics(numeric_series, second_result)
        else:
            result = combined_result
            expert_statistics = calculate_combined_expert_statistics(
                numeric_series, combined_result
            )

        row_digit_mappings = tuple(
            RowDigitMapping(index=index, first=digits[0], second=digits[1])
            for index, digits in zip(numeric_series.index, digit_pairs, strict=True)
            if digits is not None
        )
        self.state.analysis_snapshot = AnalysisSnapshot(
            mode=selected_mode,
            preprocessing_options=replace(options),
            preprocessing_preview=preview,
            suitability=assessment,
            result=result,
            expert_statistics=expert_statistics,
            row_digit_mappings=row_digit_mappings,
        )
        return result

    def configure_preprocessing(self, options: PreprocessingOptions) -> PreprocessingPreview:
        if options != self.state.preprocessing_options:
            self._invalidate_snapshot()
        self.state.preprocessing_options = options
        _series, preview = apply_preprocessing(self._raw_selected_series(), options)
        return preview

    def _invalidate_snapshot(self) -> None:
        self.state.analysis_snapshot = None

    def _raw_selected_series(self) -> pd.Series:
        if self.state.dataframe is None or self.state.selected_column is None:
            raise ValueError("A file and column must be selected before analysis.")
        return self.state.dataframe[self.state.selected_column]

    def _preprocessed_series(self) -> pd.Series:
        series, _preview = apply_preprocessing(
            self._raw_selected_series(), self.state.preprocessing_options
        )
        return series

    def check_suitability(self) -> SuitabilityAssessment:
        metrics = compute_suitability_metrics(
            self._preprocessed_series(), self._raw_selected_series()
        )
        return assess_suitability(metrics)

    def drill_down(self, digit: int) -> pd.DataFrame:
        """Return original rows for a first digit (compatibility wrapper)."""
        return self.drill_down_digit(DigitPosition.FIRST, digit)

    def drill_down_digit(self, position: DigitPosition, digit: int) -> pd.DataFrame:
        """Return original rows matching a digit in the stored analysis snapshot."""
        dataframe = self.state.dataframe
        snapshot = self.state.analysis_snapshot
        if dataframe is None or snapshot is None:
            raise ValueError("Run an analysis before showing matching rows.")
        if position is DigitPosition.FIRST and snapshot.mode is AnalysisMode.SECOND:
            raise ValueError("The current analysis does not include first-digit results.")
        if position is DigitPosition.SECOND and snapshot.mode is AnalysisMode.FIRST:
            raise ValueError("The current analysis does not include second-digit results.")

        matching_index = [
            mapping.index
            for mapping in snapshot.row_digit_mappings
            if (mapping.first if position is DigitPosition.FIRST else mapping.second) == digit
        ]
        return dataframe.loc[matching_index]
