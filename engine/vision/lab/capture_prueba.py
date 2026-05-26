# script encargado de capturar la pantalla

# Debe haber funciones para cada una de las zonas deseadas a capturar. Mirar de ver como granularizar las zonas.
# Entiendo que quizás este sería un buen punto de partida en el que generar etiquetas de cada atributo, y traspasarlo
# de aquí?
# No porque no sabría de qué se trata cada row, solo puedo diferenciar por rows. En ocr debería de ser donde asignar
# lo interpretado a cada atributo. Ahí es donde va.

import mss
import numpy
import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


with mss.mss() as sc_sht:
    monitor = sc_sht.monitors[1]
    captura = sc_sht.grab(monitor)

    img = numpy.array(captura)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    cv2.imwrite("pantalla.png", img)
#    cv2.imshow("Pantalla", img)    mostrar captura
#    cv2.waitKey(0)                 esperar con programa abierto
#    cv2.destroyAllWindows()        cerrar todo

# ---------- 2) PREPROCESADO (mejora OCR) ----------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] esto es para pasarlo a puro blanco y negro

cv2.imwrite("pantalla_bn.png", gray)

# ---------- 3) OCR GLOBAL CON COORDENADAS ----------

data = pytesseract.image_to_data(
    gray,
    output_type = pytesseract.Output.DICT,
    lang = "spa+eng",
    config = "--psm 11"
)

anchor = None
target_word = "ZAPATEROMAGO"

for i, text in enumerate(data["text"]):
    # Limpiar caracteres no alfanuméricos y pasar a mayúsculas
    word = re.sub(r'[^A-Z0-9]', '', text.upper())

    if word == target_word:
        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]
        anchor = (x, y, w, h)
        print("✅ Ancla encontrada:", anchor, "->", text.strip())
        break

if anchor is None:
     raise RuntimeError("❌ No se encontró ZAPATEROMAGO")

# # ---------- 3.1) LISTAR TODAS LAS PALABRAS DETECTADAS ----------
# data = pytesseract.image_to_data(
#     gray,
#     output_type=pytesseract.Output.DICT,
#     config="--psm 6"
# )

# print("📝 Palabras detectadas:")
#
# for i, text in enumerate(data["text"]):
#     word = text.strip()
#     if word:  # ignorar strings vacíos
#         x = data["left"][i]
#         y = data["top"][i]
#         w = data["width"][i]
#         h = data["height"][i]
#         print(f"'{word}' en ({x}, {y}, {w}, {h})")


# ---------- 4) DIBUJAR ANCLA (DEBUG VISUAL) ----------
x, y, w, h = anchor
debug_img = img.copy()
cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imwrite("debug_ancla.png", debug_img)

# ---------- 5) CALCULAR ZONA RELATIVA ----------
zone_x = x + w + 10
zone_y = max(0, y - 5)
zone_w = 250
zone_h = h + 10

roi = img[zone_y:zone_y + zone_h, zone_x:zone_x + zone_w]

# ---------- 6) OCR LOCALIZADO ----------
roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi_gray = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

value = pytesseract.image_to_string(
    roi_gray,
    config="--psm 7"
).strip()

print("📄 Valor leído:", value)

# ---------- 7) GUARDAR RESULTADOS ----------
cv2.imwrite("pantalla.png", img)
cv2.imwrite("zona_leida.png", roi)