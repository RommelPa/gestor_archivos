from PySide6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem,
    QLabel, QVBoxLayout, QPushButton,
    QFileDialog, QHeaderView, QHBoxLayout, QAbstractItemView
)
from PySide6.QtCore import Qt

from app.core.history_manager import load_history
from app.core.pdf_exporter import export_history_to_pdf


class HistoryPanel(QWidget):

    def __init__(self):
        super().__init__()
        title_layout = QHBoxLayout()

        self.lbl_title = QLabel("Historial")
        self.lbl_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #333;
        """)

        self.badge = QLabel("0 registro(s)")
        self.badge.setStyleSheet("""
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 12px;
        """)

        title_layout.addWidget(self.lbl_title)
        title_layout.addStretch()
        title_layout.addWidget(self.badge)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Archivo", "Destino", "Fecha"])

        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.ElideNone)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(2, 150)

        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #dfe3e8;
                border-radius: 6px;
                font-size: 13px;
            }
            QHeaderView::section {
                background: #f5f7fa;
                font-weight: bold;
                padding: 6px;
                border: none;
                color: #57606a;
            }
        """)

        self.btn_export = QPushButton("Exportar historial a PDF")
        self.btn_export.setStyleSheet("""
            background: #d32f2f;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
            color: white;
        """)

        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_export)

        self.setLayout(layout)

        self.load_history_to_ui()
        self.btn_export.clicked.connect(self.export_pdf)

    def _create_wrapped_label(self, text: str) -> QLabel:
        """Forzar break-all usando QLabel dentro de la celda."""
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setTextInteractionFlags(Qt.NoTextInteraction)
        lbl.setStyleSheet("""
            QLabel {
                padding: 4px;
                color: #333;
            }
        """)
        return lbl

    def load_history_to_ui(self):
        history = load_history()
        self.table.setRowCount(0)

        for entry in history:
            self.add_entry(entry)

        self.update_badge()

    def add_entry(self, entry):
        row = self.table.rowCount()
        self.table.insertRow(row)

        archivo = entry["filename"]
        destino = entry["destino"]
        fecha = entry["fecha"]

        self.table.setCellWidget(row, 0, self._create_wrapped_label(archivo))
        self.table.setCellWidget(row, 1, self._create_wrapped_label(destino))

        item_fecha = QTableWidgetItem(fecha)
        item_fecha.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item_fecha)

        self.table.resizeRowToContents(row)

        self.update_badge()

    def update_badge(self):
        total = self.table.rowCount()
        self.badge.setText(f"{total} registro(s)")

    def export_pdf(self):
        history = load_history()
        if not history:
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar historial como PDF",
            "historial.pdf",
            "PDF (*.pdf)"
        )

        if ruta:
            export_history_to_pdf(history, ruta)
