"""
Agrego documentación para probar
"""
import os
import io
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from constants import *
from urllib.parse import quote_plus

def ensure_dir(path):
    os.makedirs(path, exist_ok=True) # para que no tire excep si la carpeta ya existe

def generar_qr(numero):
    """
    Esta función es la que te arma el qr que te manda a enviar un wpp al contacto
    """
    url = f'https://wa.me/{numero}'
    qr_img = qrcode.make(url)
    qr_io = io.BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    return ImageReader(qr_io)

def generar_qr_contacto(nombre, apellido, numero):
    """
    Esta función es la te arma el qr que te manda a agendar el contacto
    """
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{apellido};{nombre}
FN:{nombre} {apellido}
TEL;TYPE=CELL:{numero}
END:VCARD"""
    qr_img = qrcode.make(vcard)
    qr_io = io.BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    return ImageReader(qr_io)

def generar_qr_check_in(DNI):
    """
    Esta función arma el qr que enviaremos por mail a los asistentes
    """
    url = f"{WEBAPP_URL}?id={quote_plus(DNI)}"
    qr_img = qrcode.make(url)
    qr_io = io.BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    return ImageReader(qr_io)

def cargar_plantilla():
    # la plantilla es un png todo en blanco jaja le podemos agregar el logo
    plantilla = Image.open(PLANTILLA_PATH).resize((int(PAGE_WIDTH), int(PAGE_HEIGHT)))
    plantilla_io = io.BytesIO()
    plantilla.save(plantilla_io, format='PNG')
    plantilla_io.seek(0)
    return ImageReader(plantilla_io)

def crear_pdf(nombre, apellido, qr_reader, plantilla_reader):
    from constants import PDF_OUTPUT_DIR

    nombre_completo = f"{nombre} {apellido}"
    pdf_filename = f"{nombre}_{apellido}.pdf"
    pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Página 1: Nombre
    c.drawImage(plantilla_reader, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2, nombre_completo)
    c.showPage()

    # Página 2: QR
    c.drawImage(plantilla_reader, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    qr_x = (PAGE_WIDTH - QR_SIZE) / 2
    qr_y = (PAGE_HEIGHT - QR_SIZE) / 2
    c.drawImage(qr_reader, qr_x, qr_y, width=QR_SIZE, height=QR_SIZE)
    c.showPage()

    c.save()
    return pdf_path


def crear_pdf_check_in(nombre, qr_reader, plantilla_reader):
    from constants import PDF_OUTPUT_DIR

    nombre_completo = f"{nombre}"
    pdf_filename = f"{nombre}.pdf"
    pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Página 1: Nombre
    c.drawImage(plantilla_reader, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2, nombre_completo)
    c.showPage()

    # Página 2: QR
    c.drawImage(plantilla_reader, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    qr_x = (PAGE_WIDTH - QR_SIZE) / 2
    qr_y = (PAGE_HEIGHT - QR_SIZE) / 2
    c.drawImage(qr_reader, qr_x, qr_y, width=QR_SIZE, height=QR_SIZE)
    c.showPage()

    c.save()
    return pdf_path
