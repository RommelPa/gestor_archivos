import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import QCoreApplication
from app.core.worker import Worker

def main():
    app = QCoreApplication(sys.argv)

    def on_progress(p):
        print("Progreso:", p)

    def on_done(path):
        print("Completado:", path)
        app.quit()

    archivo = r"C:\Windows\notepad.exe"
    destino = r"C:\Temp\gestor_test"

    w = Worker(archivo, destino, enviar_correo=False)
    w.progreso.connect(on_progress)
    w.completado.connect(on_done)
    w.start()

    app.exec()

if __name__ == "__main__":
    main()
