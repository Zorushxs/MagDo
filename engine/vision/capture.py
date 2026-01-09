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
import pytesseract
import time

# ---------- 1) Captura de pantalla ----------
def capture_screen(alto_fisico, monitor_index=1):
    with mss.mss() as sct:

        if not os.path.exists("screenshots/originals"):
            os.makedirs("screenshots/originals")

        monitor = sct.monitors[monitor_index]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        # Convertimos de BGRA a BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        save_Path = f"screenshots/originals/{alto_fisico}_screenshot.png"
        cv2.imwrite(save_Path, img)

        return img

# ---------- 2) Pasar a gris ----------
def to_gray(alto_fisico, img):

    if not os.path.exists("screenshots/gray"):
        os.makedirs("screenshots/gray")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_Path = f"screenshots/gray/{alto_fisico}_screenshot.png"
    cv2.imwrite(save_Path, img)

    return img

# ---------- 3) Recortar un box por píxeles ----------
def crop_box(img, x, y, w, h):
    """
    img: numpy array
    x, y: coordenadas superior izquierda
    w, h: ancho y alto del box
    """
    return img[y:y+h, x:x+w]

# ---------- 4) Reeditar imagen debug ----------------
def gray_debug(alto_fisico, img, x, y, w, h):
    cv2.rectangle(img, (x, y), (x + w, y + h), (80, 200, 120), 1)
    save_Path = f"screenshots/gray_debug/{alto_fisico}_screenshot.png"
    cv2.imwrite(save_Path, img)

# ---------- 5) Ejemplo de uso ----------
if __name__ == "__main__":

#    print("Por favor, introduce el número de monitor:")
#    entrada = input() # Captura la entrada como un string (ej: "1")
#    indice_monitor = int(entrada)

    monitor = obtener_detalles_monitor(0)
    alto_fisico = monitor['alto_físico']

    # Capturamos la pantalla completa
    screen = capture_screen(alto_fisico, 0 + 1)

    # Convertimos a gris
    gray_screen = to_gray(alto_fisico, screen)

    # Obtenemos el box
    boxes = BOXES_CONFIG[alto_fisico]

    # Iteramos el objeto completo
    start = time.perf_counter()
    for i, (row_name, columns) in enumerate(boxes.items()):
        if i == 0:
            debug_img = cv2.cvtColor(gray_screen, cv2.COLOR_GRAY2BGR)
            if not os.path.exists("screenshots/gray_debug"):
                os.makedirs("screenshots/gray_debug")
            save_Path = f"screenshots/gray_debug/{alto_fisico}_screenshot.png"
            cv2.imwrite(save_Path, debug_img)

        subfolder = f"boxes/{alto_fisico}/{row_name}"

        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        for col_name, box_obj in columns.items():
            x, y, w, h = box_obj.coords

            crop = crop_box(gray_screen, x, y, w, h)
            gray_debug(alto_fisico, debug_img, x, y, w, h)

            # TODO extract to ocr, and use ocr instead pytesseract due to time
            recorte_grande = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            texto_completo = pytesseract.image_to_string(
                recorte_grande,
                lang="spa+eng",
                config="--psm 11"
            ).strip()

            print(f"Resultado: {texto_completo}")


            save_Path = f"{subfolder}/{row_name}_{col_name}.png"

            cv2.imwrite(save_Path, recorte_grande)

    end = time.perf_counter()
    print(f"Tiempo del bucle: {end - start:.6f} segundos")