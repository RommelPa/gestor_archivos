from PySide6.QtCore import QThread, Signal
from app.core.file_manager import mover_archivo
from app.core.email_manager import preparar_correo
import os
import time

class Worker(QThread):
    progreso = Signal(int)
    completado = Signal(list)

    def __init__(self, archivos: list, destino: str, enviar_correo: bool = False):
        super().__init__()
        self.archivos = archivos
        self.destino = destino
        self.enviar_correo = enviar_correo

    def run(self):
        procesados = []
        total = len(self.archivos)

        for i, archivo in enumerate(self.archivos):

            # Validación: archivo desapareció
            if not os.path.exists(archivo):
                print(f"[WORKER] Archivo no encontrado: {archivo}")
                continue

            # Validación: bloqueado o sin permisos
            if not os.access(archivo, os.R_OK):
                print(f"[WORKER] Sin permisos para leer: {archivo}")
                continue

            # Validación: archivo ya existe en destino
            nombre = os.path.basename(archivo)
            destino_final = os.path.join(self.destino, nombre)

            if os.path.exists(destino_final):
                print(f"[WORKER] Archivo ya existe en destino, se omite: {destino_final}")
                continue

            time.sleep(0.3)  # simula trabajo

            archivo_final = mover_archivo(archivo, self.destino)

            if archivo_final:
                procesados.append(archivo_final)

            avance = int(((i + 1) / total) * 100)
            self.progreso.emit(avance)

        if self.enviar_correo and procesados:
            preparar_correo(self.destino, procesados)

        self.completado.emit(procesados)