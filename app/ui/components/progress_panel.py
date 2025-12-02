import os
from PySide6.QtWidgets import (
    QWidget, QPushButton, QCheckBox, QVBoxLayout, QMessageBox
)
from app.core.worker import Worker
from app.ui.components.progress_bar import ProgressBarReact

class ProgressPanel(QWidget):
    """
    Panel que gestiona el Worker: botón de procesar, checkbox e indicador de progreso.
    """
    def __init__(self):
        super().__init__()

        self.worker = None

        self.chk_email = QCheckBox("Preparar correo en Outlook")
        self.btn_run = QPushButton("Procesar")
        self.progress = ProgressBarReact()

        layout = QVBoxLayout()
        layout.addWidget(self.chk_email)
        layout.addWidget(self.progress)
        layout.addWidget(self.btn_run)
        layout.addStretch()
        self.setLayout(layout)

    def start_process(self, archivos, destino):
        """
        Valida todo antes de iniciar el Worker.
        """
        if not archivos:
            QMessageBox.warning(self, "Sin archivos", "Agrega uno o más archivos primero.")
            return

        for a in archivos:
            if not os.path.exists(a):
                QMessageBox.critical(self, "Archivo perdido", f"No existe:\n{a}\n\nElimínalo de la lista.")
                return
            if not os.access(a, os.R_OK):
                QMessageBox.critical(self, "Archivo bloqueado", f"El archivo está siendo usado:\n{a}")
                return

        if not destino:
            QMessageBox.warning(self, "Destino requerido", "Selecciona una carpeta destino.")
            return

        if not os.path.isdir(destino):
            QMessageBox.critical(self, "Destino inválido", "La carpeta destino no existe.")
            return

        if not os.access(destino, os.W_OK):
            QMessageBox.critical(self, "Sin permisos", "No tienes permisos de escritura en la carpeta destino.")
            return

        if self.chk_email.isChecked():
            try:
                import win32com.client
                win32com.client.Dispatch("Outlook.Application")
            except:
                QMessageBox.critical(self, "Outlook no disponible", "No se puede iniciar Outlook.")
                return

        self.btn_run.setEnabled(False)
        self.progress.setValue(0)

        self.worker = Worker(
            archivos,
            destino,
            self.chk_email.isChecked()
        )

        self.worker.progreso.connect(self.progress.setValue)
        self.worker.completado.connect(self.on_completed)
        self.worker.start()

    def on_completed(self, rutas):
        self.btn_run.setEnabled(True)
        self.progress.setValue(100)