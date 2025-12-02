import os
import shutil

def mover_archivo(ruta_archivo: str, ruta_destino: str) -> str:
    """
    Copia el archivo a la carpeta destino y devuelve la ruta final.
    No borra el original (usa copy por seguridad).
    """
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino, exist_ok=True)

    archivo_final = os.path.join(ruta_destino, os.path.basename(ruta_archivo))
    shutil.copy(ruta_archivo, archivo_final)
    return archivo_final