"""Packaging metadata regression tests."""

from __future__ import annotations

import tomllib
from pathlib import Path


def test_translation_json_declared_as_package_data():
    """Built wheels must include GUI translation files used by legacy PyQt UI."""
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert package_data["src.gui"] == ["translations/*.json"]
