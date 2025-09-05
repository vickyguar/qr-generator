import pandas as pd
import os
import zipfile
from constants import *
from utils import *
from email_cesabi import *
from dotenv import load_dotenv


def cargar_dataframe():
    # Aca habria que hacer un pd.read_csv con el archivo de inscriptos que me imagino que tiene esas columnas
    return pd.read_csv("repres.csv")


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
    
    with open(body_template_path, 'r', encoding='utf-8') as f:
        body_template = f.read()
    
    for _, row in df.iterrows():
        nombre = row['nombre']
        apellido = row['apellido']
        #numero = str(row['mobilephone']).replace(" ", "").replace("+", "")
        DNI = row['DNI']
        recipient_email = row["email"]
        body = body_template.format(participant_name=nombre)
        #print(body)
        pdf_path = generar_pdfs(nombre, apellido, DNI, "check-in")
        send_email(sender_email, password, sender_name, recipient_email, subject, body, pdf_path)

if __name__ == "__main__":
    main()
