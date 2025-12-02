import os
import sys
from PySide6.QtWidgets import QApplication
from app.ui.window import MainWindow


def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta correcta tanto en desarrollo como dentro del .exe (PyInstaller).
    """
    if hasattr(sys, "_MEIPASS"):
        # Ejecutable PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Código fuente
        return os.path.join(os.path.dirname(__file__), relative_path)


def main():
    app = QApplication([])

    # Cargar estilo QSS
    qss_path = resource_path("ui/styles/main.qss")

    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print("⚠ No se encontró main.qss en:", qss_path)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    # IMPORTANTE PARA IMPORTAR app.*
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    main()
