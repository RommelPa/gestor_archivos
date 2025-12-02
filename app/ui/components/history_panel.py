from PySide6.QtWidgets import QWidget, QListWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from app.core.history_manager import load_history
from app.core.pdf_exporter import export_history_to_pdf

class HistoryPanel(QWidget):
    """
    Panel lateral para mostrar historial.
    """
    def __init__(self):
        super().__init__()

        self.lista = QListWidget()
        self.btn_export = QPushButton("Exportar historial a PDF")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Historial"))
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_export)
        self.setLayout(layout)

        self.load_history_to_ui()
        self.btn_export.clicked.connect(self.export_pdf)

    def load_history_to_ui(self):
        """Carga historial desde JSON a la lista visual"""
        self.lista.clear()
        history = load_history()

        for entry in history:
            texto = f"{entry['filename']}  →  {entry['destino']}  ({entry['fecha']})"
            self.lista.addItem(texto)

    def add_entry(self, entry):
        """Añade una entrada al panel UI"""
        texto = f"{entry['filename']}  →  {entry['destino']}  ({entry['fecha']})"
        self.lista.addItem(texto)

    def export_pdf(self):
        """Exporta historial a un PDF elegible por el usuario."""
        history = load_history()

        if not history:
            print("No hay historial para exportar.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar historial como PDF",
            f"historial_{self._timestamp()}.pdf",
            "PDF Files (*.pdf)"
        )

        if ruta:
            export_history_to_pdf(history, ruta)
            print(f"Historial exportado a PDF: {ruta}")

    def _timestamp(self):
        """Genera timestamp para nombres de archivo"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")