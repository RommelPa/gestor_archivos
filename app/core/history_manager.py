import json
import os
from datetime import datetime

HISTORY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "resources",
    "history.json"
)

def load_history():
    """Carga el historial desde history.json"""
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history):
    """Guarda el historial completo"""
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def add_entry(filename, destino):
    """Agrega una entrada al historial"""
    history = load_history()

    entry = {
        "filename": filename,
        "destino": destino,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(entry)
    save_history(history)

    return entry
