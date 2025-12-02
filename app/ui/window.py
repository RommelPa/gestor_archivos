from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget, QHBoxLayout, QVBoxLayout
from app.ui.components.file_selector import FileSelector
from app.ui.components.progress_panel import ProgressPanel
from app.ui.components.history_panel import HistoryPanel
from app.ui.components.card import Card
from app.core.history_manager import add_entry
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Archivos - PySide6")
        self.setMinimumSize(900, 500)

        # Componentes
        self.file_selector = FileSelector()
        self.progress_panel = ProgressPanel()
        self.history_panel = HistoryPanel()

        # PANEL IZQUIERDO
        left_side = QVBoxLayout()
        left_side.setContentsMargins(20, 20, 20, 20)
        left_side.setSpacing(20)

        left_side.addWidget(Card(self.file_selector))
        left_side.addWidget(Card(self.progress_panel))
        left_side.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_side)
        left_widget.setObjectName("LeftPanel")
        left_widget.setMinimumWidth(420)

        # PANEL DERECHO
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(Card(self.history_panel))
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)
        right_widget.setLayout(right_layout)
        right_widget.setObjectName("RightPanel")
        right_widget.setMinimumWidth(250)

        # LAYOUT PRINCIPAL
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

        container = QWidget()
        container.setLayout(main_layout)
        container.setObjectName("CentralContainer")

        self.setCentralWidget(container)

        # Conectar eventos
        self.progress_panel.btn_run.clicked.connect(self.on_run_clicked)

    def on_process_completed(self, archivos_finales):
        if not archivos_finales:
            QMessageBox.critical(
                self,
                "Error",
                "Ningún archivo pudo procesarse.\n"
                "Revisa permisos, rutas o si los archivos están abiertos."
            )
            return

        if len(archivos_finales) < len(self.file_selector.archivos):
            QMessageBox.warning(
                self,
                "Advertencia",
                "Algunos archivos no pudieron procesarse.\n"
                "Revisa permisos o archivos abiertos."
            )

        for archivo_final in archivos_finales:
            filename = os.path.basename(archivo_final)
            destino = os.path.dirname(archivo_final)
            entry = add_entry(filename, destino)
            self.history_panel.add_entry(entry)

        QMessageBox.information(
            self,
            "Completado",
            f"Se procesaron {len(archivos_finales)} archivo(s)."
        )

    def on_run_clicked(self):
        self.progress_panel.start_process(
            self.file_selector.archivos,
            self.file_selector.ruta_destino
        )
        self.progress_panel.worker.completado.connect(self.on_process_completed)
