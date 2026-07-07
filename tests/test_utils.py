"""Tests for utility helpers."""

from __future__ import annotations

import pytest

from src.utils.helper import load_translations


def test_load_translations_from_package_resources():
    translations = load_translations("en")

    assert translations["setup_tab"] == "Setup"
    assert translations["success_message"]


def test_load_translations_rejects_unknown_language():
    with pytest.raises(ValueError, match="Unsupported language"):
        load_translations("../en")
