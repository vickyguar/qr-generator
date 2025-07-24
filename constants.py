from PIL import Image

PLANTILLA_PATH = "Plantilla.png"
# TODO: Plantilla2 (para el frente)

with Image.open(PLANTILLA_PATH) as img:
    PAGE_WIDTH, PAGE_HEIGHT = img.size
    PAGE_WIDTH = PAGE_WIDTH // 2
    PAGE_HEIGHT = PAGE_HEIGHT // 2

QR_SIZE = 150  
PDF_OUTPUT_DIR = "pdf_contactos"
ZIP_OUTPUT_PATH = "contactos_qr_congreso.zip"
