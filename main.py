import pandas as pd
import os
import zipfile
from constants import PDF_OUTPUT_DIR, ZIP_OUTPUT_PATH
from utils import ensure_dir, generar_qr, generar_qr_contacto, cargar_plantilla, crear_pdf

def cargar_dataframe():
    # Aca habria que hacer un pd.read_csv con el archivo de inscriptos que me imagino que tiene esas columnas
    return pd.DataFrame({
        'nombre': ['Ramiro', 'Juan'],
        'apellido': ['Gijón', 'Augusto'],
        'mobilephone': ['92604056182', '93814473695']
    })

def generar_pdfs(df):
    ensure_dir(PDF_OUTPUT_DIR)
    plantilla_reader = cargar_plantilla()
    pdf_paths = []

    for _, row in df.iterrows():
        nombre = row['nombre']
        apellido = row['apellido']
        numero = str(row['mobilephone']).replace(" ", "").replace("+", "")
        #Comentar y descomentar acá para probar con los dos tipos de qr
        #qr_reader = generar_qr(numero)
        qr_reader = generar_qr_contacto(nombre, apellido, numero)
        pdf_path = crear_pdf(nombre, apellido, qr_reader, plantilla_reader)
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
