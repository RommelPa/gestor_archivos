import win32com.client as win32

def main():
    try:
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.To = "tu@correo.com"
        mail.Subject = "Prueba desde pywin32"
        mail.Body = "Si ves esto, pywin32 -> Outlook ok."
        # No lo enviamos: solo mostramos el objeto y la clase
        print("Outlook dispatch OK:", type(outlook))
        print("Mail object OK:", type(mail))
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    main()
