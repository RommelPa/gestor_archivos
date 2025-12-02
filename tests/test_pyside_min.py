from PySide6.QtWidgets import QApplication, QLabel
import sys

def main():
    app = QApplication(sys.argv)
    label = QLabel("PySide6 funcionando ✅")
    label.setMinimumSize(300, 80)
    label.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
