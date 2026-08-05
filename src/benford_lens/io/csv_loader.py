"""CSV loading with best-effort automatic encoding detection.

No external file content is ever transmitted anywhere; this module only
reads from the local filesystem path it is given.
"""

from __future__ import annotations

import pandas as pd

_ENCODING_CANDIDATES: tuple[str, ...] = ("utf-8-sig", "utf-8", "cp949", "euc-kr", "latin-1")


class CsvLoadError(Exception):
    """Raised when a CSV file cannot be read with any supported encoding."""


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame, trying encodings in order.

    ``latin-1`` never raises a decode error, so it is used last as a
    catch-all rather than a real content-based detector.
    """
    last_error: Exception | None = None
    for encoding in _ENCODING_CANDIDATES:
        try:
            return pd.read_csv(path, encoding=encoding)
        except (UnicodeDecodeError, UnicodeError) as exc:
            last_error = exc
            continue
        except OSError as exc:
            raise CsvLoadError(f"Could not open {path}: {exc}") from exc
    raise CsvLoadError(f"Could not decode {path} with any supported encoding") from last_error
