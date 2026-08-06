import re
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_I18N_DIR = _PROJECT_ROOT / "resources" / "i18n"
_LANGUAGE_CODES = ("ko", "zh", "ja", "es", "fr", "ru")
_PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def _catalog_messages(language_code: str) -> dict[tuple[str, str], str]:
    root = ET.parse(_I18N_DIR / f"benford_lens_{language_code}.ts").getroot()
    messages: dict[tuple[str, str], str] = {}
    for context in root.findall("context"):
        context_name = context.findtext("name") or ""
        for message in context.findall("message"):
            source = message.findtext("source") or ""
            translation = message.findtext("translation") or ""
            messages[(context_name, source)] = translation
    return messages


@pytest.mark.parametrize("language_code", _LANGUAGE_CODES)
def test_translation_catalog_is_complete_and_preserves_placeholders(language_code):
    reference = _catalog_messages("ko")
    catalog = _catalog_messages(language_code)

    assert len(reference) == 93
    assert catalog.keys() == reference.keys()
    assert all(translation.strip() for translation in catalog.values())
    for (_context, source), translation in catalog.items():
        assert set(_PLACEHOLDER_RE.findall(translation)) == set(_PLACEHOLDER_RE.findall(source))


@pytest.mark.parametrize("language_code", _LANGUAGE_CODES)
def test_compiled_translation_catalog_exists(language_code):
    compiled_catalog = _I18N_DIR / f"benford_lens_{language_code}.qm"

    assert compiled_catalog.exists()
    assert compiled_catalog.stat().st_size > 0
