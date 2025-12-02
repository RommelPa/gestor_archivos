import os
import json
import sys
from datetime import datetime

def get_history_path():
    """
    Devuelve la ruta donde se guardará history.json.
    En modo ejecutable → AppData/Local/GestorArchivos
    En desarrollo → resources/history.json
    """
    if hasattr(sys, "_MEIPASS"):
        # Modo ejecutable
        base = os.path.join(os.getenv("LOCALAPPDATA"), "GestorArchivos")
    else:
        # Modo desarrollo
        base = os.path.join(
            os.path.dirname(__file__), "..", "..", "resources"
        )

    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "history.json")

HISTORY_PATH = get_history_path()

def load_history():
    """Carga el historial desde JSON."""
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    """Guarda el historial completo."""
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def add_entry(filename, destino):
    """Agrega una entrada al historial con fecha y hora."""
    history = load_history()

    entry = {
        "filename": filename,
        "destino": destino,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(entry)
    save_history(history)

    return entry