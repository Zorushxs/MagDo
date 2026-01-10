# script encargado de capturar la pantalla

# Debe haber funciones para cada una de las zonas deseadas a capturar. Mirar de ver como granularizar las zonas.
# Entiendo que quizás este sería un buen punto de partida en el que generar etiquetas de cada atributo, y traspasarlo
# de aquí?
# No porque no sabría de qué se trata cada row, solo puedo diferenciar por rows. En ocr debería de ser donde asignar
# lo interpretado a cada atributo. Ahí es donde va.

import mss
import numpy as np
import cv2
import os
from screen_detection import obtener_detalles_monitor
from boxes_config import BOXES_CONFIG
import time
from ocr import OCREngine

# ---------- 1) Captura y Preparación --------
def get_processed_screen(alto_fisico, monitor_index=1):
    with mss.mss() as sct:
        # 1. Captura
        screenshot = sct.grab(sct.monitors[monitor_index])
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR) # Convertimos de BGRA a BGR

        # 2. Convertir a gris
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Guardado único de originales
        os.makedirs(f"screenshots/originals", exist_ok=True)
        os.makedirs(f"screenshots/gray", exist_ok=True)
        cv2.imwrite(f"screenshots/originals/{alto_fisico}_screenshot.png", img)
        cv2.imwrite(f"screenshots/gray/{alto_fisico}_screenshot.png", gray_img)

        return gray_img

# ---------- 3) Recortar, reescalar, guardar y leer --
def crop_rsr(alto_fisico, boxes, gray_screen):

    debug_img = cv2.cvtColor(gray_screen, cv2.COLOR_GRAY2BGR)
    os.makedirs(f"screenshots/gray_debug", exist_ok=True)

    start = time.perf_counter()
    with OCREngine() as ocr:
        for row_name, columns in boxes.items():
            subfolder = f"boxes/{alto_fisico}/{row_name}"
            os.makedirs(subfolder, exist_ok=True)

            for col_name, box_obj in columns.items():
                x, y, w, h = box_obj.coords

                cv2.rectangle(debug_img, (x, y), (x + w, y + h), (80, 200, 120), 1)

                # Uso de la api OCR
                crop = gray_screen[y:y+h, x:x+w]
                recorte_grande = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
                texto_completo = ocr.read_image(recorte_grande)
                print(f"Resultado: {texto_completo}")

                cv2.imwrite(f"{subfolder}/{row_name}_{col_name}.png", recorte_grande)

        cv2.imwrite(f"screenshots/gray_debug/{alto_fisico}_screenshot.png", debug_img)

    end = time.perf_counter()
    print(f"Tiempo del bucle: {end - start:.6f} segundos")

# ---------- 5) Ejemplo de uso ----------
if __name__ == "__main__":

#    print("Por favor, introduce el número de monitor:")
#    entrada = input() # Captura la entrada como un string (ej: "1")
#    indice_monitor = int(entrada)

    monitor = obtener_detalles_monitor(0)
    alto_fisico = monitor['alto_físico']

    # Capturamos la pantalla completa y convertimos a gris
    gray_screen = get_processed_screen(alto_fisico, 0 + 1)

    # Obtenemos el box
    boxes = BOXES_CONFIG[alto_fisico]

    crop_rsr(alto_fisico, boxes, gray_screen)