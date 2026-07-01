"""Packaging metadata regression tests."""

from __future__ import annotations

from pathlib import Path


def test_translation_json_declared_as_package_data():
    """Built wheels must include GUI translation files used by legacy PyQt UI."""
    pyproject = Path("pyproject.toml").read_text()

    assert "[tool.setuptools.package-data]" in pyproject
    assert '"src.gui" = ["translations/*.json"]' in pyproject
