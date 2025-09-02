import pandas as pd
import os
import zipfile
from constants import *
from utils import *

def cargar_dataframe():
    # Aca habria que hacer un pd.read_csv con el archivo de inscriptos que me imagino que tiene esas columnas
    return pd.DataFrame({
    'nombre': ['Gonzalo Grau', 'Chiche Gelblung', 'Marcelo Polino', 'Fabricio Ballarini', 'Victoria Guarnieri'],
    #'apellido': ['Gijón', 'Augusto'],
    #'mobilephone': ['1111', '1111'],
    'DNI' : ['43630060', '21953101', '22001847', '31858799', '44555989']
})

def generar_pdfs(df):
    ensure_dir(PDF_OUTPUT_DIR)
    plantilla_reader = cargar_plantilla()
    pdf_paths = []

    for _, row in df.iterrows():
        nombre = row['nombre']
        #apellido = row['apellido']
        #numero = str(row['mobilephone']).replace(" ", "").replace("+", "")
        DNI = row['DNI']
        #Comentar y descomentar acá para probar con los dos tipos de qr
        #qr_reader = generar_qr(numero)
        #qr_reader = generar_qr_contacto(nombre, apellido, numero)
        qr_reader = generar_qr_check_in(DNI)
        pdf_path = crear_pdf_check_in(nombre, qr_reader, plantilla_reader)
        pdf_paths.append(pdf_path)
        print(f"PDF generado: {pdf_path}")

    return pdf_paths

def comprimir_pdfs(pdf_paths):
    with zipfile.ZipFile(ZIP_OUTPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdf_paths:
            zipf.write(pdf, os.path.basename(pdf))
    print(f"\nArchivo ZIP creado: {ZIP_OUTPUT_PATH}")

def main():
    df = cargar_dataframe() # cuando este la lista de inscriptos pasar x acá
    pdfs = generar_pdfs(df) # arma pdf
    comprimir_pdfs(pdfs) # comprime todo

if __name__ == "__main__":
    main()
