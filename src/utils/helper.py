# src/utils/helper.py

import json
import os

def load_translations(language_code: str) -> dict:
    file_path = os.path.join(os.path.dirname(__file__), f"../gui/translations/{language_code}.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations