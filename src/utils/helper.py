# src/utils/helper.py

import json
from importlib import resources


SUPPORTED_LANGUAGES = {"en", "ja"}


def load_translations(language_code: str) -> dict:
    """Load GUI translation JSON from packaged resources."""
    if language_code not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language {language_code!r}. "
            f"Supported languages: {sorted(SUPPORTED_LANGUAGES)}"
        )

    translation_path = resources.files("src.gui").joinpath("translations", f"{language_code}.json")
    with translation_path.open("r", encoding="utf-8") as file:
        return json.load(file)
