"""Preprocessing pipeline (Analysis Engine — no UI dependency).

Applies user-chosen handling rules to a raw column before Benford analysis;
never decides on its own which values are "wrong" — every rule here is an
explicit, user-selectable option, per AGENTS.md.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal

import pandas as pd

NegativeHandling = Literal["keep", "absolute", "exclude"]
ZeroHandling = Literal["keep", "exclude"]
DecimalHandling = Literal["as_is", "round", "truncate"]
BlankHandling = Literal["exclude"]
DuplicateHandling = Literal["keep", "exclude"]

_SAMPLE_SIZE = 5
_CURRENCY_STRIP_RE = re.compile(r"[^\d.\-]")


@dataclass
class PreprocessingOptions:
    negative_handling: NegativeHandling = "absolute"
    zero_handling: ZeroHandling = "exclude"
    decimal_handling: DecimalHandling = "as_is"
    blank_handling: BlankHandling = "exclude"
    duplicate_handling: DuplicateHandling = "keep"
    string_to_number: bool = True


@dataclass
class PreprocessingPreview:
    total_before: int
    total_after: int
    excluded_negative: int
    excluded_zero: int
    excluded_blank: int
    excluded_non_numeric: int
    sample_before: list[object]
    sample_after: list[float]


def _coerce_string_to_number(value: object) -> object:
    if not isinstance(value, str):
        return value
    stripped = _CURRENCY_STRIP_RE.sub("", value)
    return stripped if stripped not in ("", "-", ".") else value


def apply_preprocessing(
    raw_series: pd.Series, options: PreprocessingOptions
) -> tuple[pd.Series, PreprocessingPreview]:
    total_before = len(raw_series)
    sample_before = list(raw_series.head(_SAMPLE_SIZE))

    original_blank_mask = raw_series.isna()
    excluded_blank = int(original_blank_mask.sum())

    working = raw_series
    if options.string_to_number:
        working = working.map(_coerce_string_to_number)
    numeric = pd.to_numeric(working, errors="coerce")

    non_numeric_mask = numeric.isna() & ~original_blank_mask
    excluded_non_numeric = int(non_numeric_mask.sum())

    # blank_handling only has one value ("exclude"): NaNs — whether they
    # started blank or failed numeric coercion — are always dropped here.
    numeric = numeric.dropna()

    excluded_negative = 0
    if options.negative_handling == "absolute":
        numeric = numeric.abs()
    elif options.negative_handling == "exclude":
        negative_mask = numeric < 0
        excluded_negative = int(negative_mask.sum())
        numeric = numeric[~negative_mask]

    excluded_zero = 0
    if options.zero_handling == "exclude":
        zero_mask = numeric == 0
        excluded_zero = int(zero_mask.sum())
        numeric = numeric[~zero_mask]

    if options.decimal_handling == "round":
        numeric = numeric.round(0)
    elif options.decimal_handling == "truncate":
        numeric = numeric.apply(math.trunc).astype(float)

    if options.duplicate_handling == "exclude":
        numeric = numeric.drop_duplicates()

    preview = PreprocessingPreview(
        total_before=total_before,
        total_after=len(numeric),
        excluded_negative=excluded_negative,
        excluded_zero=excluded_zero,
        excluded_blank=excluded_blank,
        excluded_non_numeric=excluded_non_numeric,
        sample_before=sample_before,
        sample_after=list(numeric.head(_SAMPLE_SIZE)),
    )
    return numeric, preview
