import os
import io
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
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
    url = f"{WEBAPP_URL}?id={DNI}"
    print(url)
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


def crear_pdf_check_in(nombre, apellido, DNI, qr_reader):
    # Fuentes y tamaños
    font_name_bold = "Helvetica-Bold"
    font_name = "Helvetica"
    font_size_name = 20
    font_size_dni = 16
    spacing = 15 

    # Calcular anchos de texto
    nombre_completo = f"{nombre} {apellido}"
    text_width_name = stringWidth(nombre_completo, font_name_bold, font_size_name)
    text_width_dni = stringWidth(f"DNI: {DNI}", font_name, font_size_dni)

    # Ancho
    content_width = max(QR_SIZE, text_width_name, text_width_dni) + 40  # margen lateral

    # Alto
    content_height = QR_SIZE + spacing + font_size_name + spacing + font_size_dni + 40  # margen superior/inferior

    # Nombre del archivo
    pdf_filename = f"{nombre} {apellido}.pdf"
    pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)

    # Crear canvas con tamaño ajustado
    c = canvas.Canvas(pdf_path, pagesize=(content_width, content_height))

    # Coordenada Y inicial (arriba del QR)
    y = content_height - 20 - QR_SIZE
    qr_x = (content_width - QR_SIZE) / 2
    c.drawImage(qr_reader, qr_x, y, width=QR_SIZE, height=QR_SIZE)

    # Nombre debajo del QR
    y -= spacing
    c.setFont(font_name_bold, font_size_name)
    c.drawCentredString(content_width / 2, y, nombre_completo)

    # DNI debajo del nombre
    y -= (spacing + font_size_name)
    c.setFont(font_name, font_size_dni)
    c.drawCentredString(content_width / 2, y, f"DNI: {DNI}")

    c.showPage()
    c.save()

    return pdf_path


def generar_pdfs(nombre, apellido=None, DNI=None, numero=None, mode="check-in"):
    """
    Genera un PDF con un QR en distintos modos:
    - check-in: genera QR con el DNI
    - vcard: genera QR con datos de contacto
    - wpp: genera QR con número de WhatsApp
    """
    assert mode in {"check-in", "vcard", "wpp"}, \
        "El parámetro mode solo puede tomar los valores check-in, vcard o wpp"

    ensure_dir(PDF_OUTPUT_DIR)

    # Selección del QR según el modo
    if mode == "check-in":
        qr_reader = generar_qr(DNI)
        pdf_path = crear_pdf_check_in(nombre, apellido, DNI, qr_reader)

    elif mode == "vcard":
        qr_reader = generar_qr_contacto(nombre, apellido, numero)
        pdf_path = crear_pdf(nombre, apellido, qr_reader)

    elif mode == "wpp":
        qr_reader = generar_qr_check_in(numero)
        pdf_path = crear_pdf(nombre, DNI, qr_reader)

    print(f"PDF generado: {pdf_path}")
    return pdf_path