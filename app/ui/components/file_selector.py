import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox
)
from app.ui.components.drop_zone import DropZone
from os.path import basename

class FileSelector(QWidget):
    """
    Selector de múltiples archivos y carpeta destino.
    """
    def __init__(self):
        super().__init__()

        self.archivos = []
        self.ruta_destino = None

        # Widgets
        self.lbl_archivo = QLabel("Archivos seleccionados:")
        self.list_archivos = QListWidget()
        self.list_archivos.setSelectionMode(QListWidget.ExtendedSelection)

        self.btn_archivo = QPushButton("Agregar archivos...")
        self.btn_eliminar = QPushButton("Eliminar archivo(s) seleccionados")

        # DropZone
        self.drop_zone = DropZone()
        self.drop_zone.fileDropped.connect(self.add_file)

        self.lbl_destino = QLabel("Destino: (ninguno)")
        self.btn_destino = QPushButton("Seleccionar carpeta destino...")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_archivo)
        layout.addWidget(self.list_archivos)
        layout.addWidget(self.btn_archivo)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.drop_zone)
        layout.addWidget(self.lbl_destino)
        layout.addWidget(self.btn_destino)

        layout.addStretch()
        self.setLayout(layout)

        # Eventos
        self.btn_archivo.clicked.connect(self.select_files)
        self.btn_destino.clicked.connect(self.select_folder)
        self.btn_eliminar.clicked.connect(self.remove_selected)

    def select_files(self):
        rutas, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos")
        for ruta in rutas:
            self.add_file(ruta)

    def add_file(self, ruta):
        """Valida y agrega un archivo a la lista."""
        if not ruta:
            return

        if not os.path.isfile(ruta):
            QMessageBox.warning(self, "Archivo inválido", f"El archivo no existe:\n{ruta}")
            return

        # Validar extensiones peligrosas
        extension = ruta.lower().split(".")[-1]
        peligrosas = ["exe", "bat", "cmd", "js", "vbs", "msi", "reg"]
        if extension in peligrosas:
            r = QMessageBox.warning(
                self,
                "Advertencia",
                f"El archivo '{os.path.basename(ruta)}' puede ser peligroso.\n\n¿Deseas agregarlo igual?",
                QMessageBox.Yes | QMessageBox.No
            )
            if r == QMessageBox.No:
                return

        # Evitar duplicados
        if ruta in self.archivos:
            QMessageBox.information(self, "Duplicado", "Este archivo ya fue agregado.")
            return

        # Evitar nombres muy largos
        if len(ruta) > 240:
            QMessageBox.warning(self, "Ruta demasiado larga", f"La ruta supera el límite de Windows:\n{ruta}")
            return

        # Validar que el archivo no esté bloqueado
        if not os.access(ruta, os.R_OK):
            QMessageBox.critical(self, "Sin permisos", f"No se puede leer el archivo:\n{ruta}")
            return

        self.archivos.append(ruta)
        self.list_archivos.addItem(os.path.basename(ruta))


    def remove_selected(self):
        selected_items = self.list_archivos.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Nada seleccionado", "Selecciona archivo(s) para eliminar.")
            return

        r = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Eliminar {len(selected_items)} archivo(s) de la lista?",
            QMessageBox.Yes | QMessageBox.No
        )
        if r == QMessageBox.No:
            return

        # Eliminar de atrás hacia adelante (no rompe índices)
        rows = sorted([self.list_archivos.row(i) for i in selected_items], reverse=True)
        for row in rows:
            self.list_archivos.takeItem(row)
            self.archivos.pop(row)

    def select_folder(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta destino")
        if carpeta:
            self.ruta_destino = carpeta
            self.lbl_destino.setText(f"Destino: {carpeta}")