import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.file_manager import mover_archivo
import tempfile

def main():
    tmp = tempfile.gettempdir()
    src = os.path.join(tmp, "test_gestor_sample.txt")
    with open(src, "w", encoding="utf-8") as f:
        f.write("Prueba mover_archivo\n")

    destino = os.path.join(tmp, "gestor_dest")
    if not os.path.exists(destino):
        os.makedirs(destino)

    final = mover_archivo(src, destino)
    print("Archivo copiado a:", final)
    print("Existe en destino?", os.path.exists(final))

if __name__ == "__main__":
    main()
