# script encargado de interpretar las capturas

# Este script se encargaría de interpretar las capturas en datos tratables por el script de lógica

# Como digo en capture, aquí es donde cada capture-row es interpretado y del map que tengo de todos los atributos
# posibles se le asigna el suyo correpondiente. ¡Importante! Creo que también se le debe asignar aquí a que row pertenece
# para que después la función de action sepa donde debe actuar si quiere tarjetear ese atributo.

import tesserocr
from PIL import Image
import os

class OCREngine:
    def __init__(self, lang='spa+eng'):
        # Ruta calculada automáticamente para encontrar tessdata
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tesseract/Tesseract-OCR/tessdata'))

        # Iniciamos el motor una sola vez al crear la clase
        self.api = tesserocr.PyTessBaseAPI(path=base_path, lang=lang, psm=tesserocr.PSM.SPARSE_TEXT) # psm=tesserocr.PSM.SINGLE_BLOCK

    def read_image(self, opencv_img):
        # Convertimos de OpenCV (numpy) a PIL
        pil_img = Image.fromarray(opencv_img)
        self.api.SetImage(pil_img)
        return self.api.GetUTF8Text().strip()

    def close(self):
        self.api.End()

    # Esto permite usar: with OCREngine() as ocr:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()