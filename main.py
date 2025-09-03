import pandas as pd
import os
import zipfile
from constants import *
from utils import *
from email_cesabi import *

def cargar_dataframe():
    # Aca habria que hacer un pd.read_csv con el archivo de inscriptos que me imagino que tiene esas columnas
    return pd.read_csv("asistentes.csv")


def generar_pdfs(nombre, DNI, apellido = None, numero = None):
    ensure_dir(PDF_OUTPUT_DIR)
    plantilla_reader = cargar_plantilla()

    #Comentar y descomentar acá para probar con los dos tipos de qr
    #qr_reader = generar_qr(numero)
    #qr_reader = generar_qr_contacto(nombre, apellido, numero)
    qr_reader = generar_qr_check_in(DNI)
    pdf_path = crear_pdf_check_in(nombre, qr_reader, plantilla_reader) # Estaria
    print(f"PDF generado: {pdf_path}")
        
    return pdf_path

def comprimir_pdfs(pdf_paths):
    with zipfile.ZipFile(ZIP_OUTPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdf_paths:
            zipf.write(pdf, os.path.basename(pdf))
    print(f"\nArchivo ZIP creado: {ZIP_OUTPUT_PATH}")

def main():
    df = cargar_dataframe() # cuando este la lista de inscriptos pasar x acá
    body_template_path = 'body_template.txt'
    
    # Load credentials from .env file
    load_dotenv()
    sender_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')
    sender_name = 'Cesabi'

    subject = f'QR de asistencia al SABI Estudiantil'
    body = open(body_template_path).read()
    
    for _, row in df.iterrows():
        nombre = row['nombre']
        #apellido = row['apellido']
        #numero = str(row['mobilephone']).replace(" ", "").replace("+", "")
        DNI = row['DNI']
        recipient_email = row["email"]
        body = body.format(participant_name=nombre)
        print(body)
        pdf_path = generar_pdfs(nombre, DNI)
        send_email(sender_email, password, sender_name, recipient_email, subject, body, pdf_path)

if __name__ == "__main__":
    main()
