import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication
from app.ui.window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Cargar estilos QSS
    qss_path = os.path.join(os.path.dirname(__file__), "ui", "styles", "main.qss")
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
