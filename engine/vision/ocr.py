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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tessdata_path = os.path.join(script_dir, '../tesseract/Tesseract-OCR/tessdata')
        # Convertimos la ruta combinada en la ruta absoluta final
        final_tessdata_path = os.path.abspath(tessdata_path)

        # Iniciamos el motor una sola vez al crear la clase
        self.api = tesserocr.PyTessBaseAPI(path=final_tessdata_path, lang=lang, psm=tesserocr.PSM.SPARSE_TEXT) # psm=tesserocr.PSM.SINGLE_BLOCK

    def read_image(self, opencv_img):
        # Convertimos de OpenCV (numpy) a PIL
        pil_img = Image.fromarray(opencv_img)
        self.api.SetImage(pil_img)
        return self.api.GetUTF8Text().strip()

    def close(self):
        self.api.End()