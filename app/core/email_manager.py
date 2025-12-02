import os
import win32com.client as win32

def preparar_correo(ruta_destino: str, archivos_finales: list, to_address: str = "prac.fmenor@egasa.com.pe"):
    """
    Prepara un correo Outlook con varios archivos adjuntos.
    """
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = to_address
        mail.Subject = "Entrega de archivos"
        mail.Body = (
            "Estimado gerente,\n\n"
            f"Adjunto los archivos movidos a la carpeta:\n{ruta_destino}\n\n"
            "Saludos."
        )

        for archivo in archivos_finales:
            if archivo and os.path.exists(archivo):
                mail.Attachments.Add(archivo)
            else:
                print("[email_manager] Archivo inexistente:", archivo)

        mail.Display()
        print("[email_manager] Correo mostrando en Outlook.")
    except Exception as e:
        print("[email_manager] Error preparando correo:", e)
