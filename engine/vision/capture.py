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

# ---------- 1) Captura de pantalla ----------
def capture_screen(monitor_index=1):
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        # Convertimos de BGRA a BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

# ---------- 2) Pasar a gris ----------
def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ---------- 3) Recortar un box por píxeles ----------
def crop_box(img, x, y, w, h):
    """
    img: numpy array
    x, y: coordenadas superior izquierda
    w, h: ancho y alto del box
    """
    return img[y:y+h, x:x+w]

# ---------- 4) Ejemplo de uso ----------
if __name__ == "__main__":
    # Capturamos la pantalla completa
    screen = capture_screen()

    # Convertimos a gris
    gray_screen = to_gray(screen)

    # Definimos varios boxes estáticos
    boxes = {
        "row0": (860, 496, 650, 30),    # x, y, w, h
        "row1": (100, 200, 150, 50),
        "row2": (400, 300, 200, 80),    # de momento trabajaré con 2 rows, ver cuantas son necesarias
        "row3": (400, 300, 200, 80),
        "row4": (400, 300, 200, 80),
        "row5": (400, 300, 200, 80),
        "row6": (400, 300, 200, 80),
        "row7": (400, 300, 200, 80),
        "row8": (400, 300, 200, 80),
        "row9": (400, 300, 200, 80)
    }

    # Recortamos y guardamos
    for name, (x, y, w, h) in boxes.items():
        if name.startswith("row"):
            subfolder = "rows"

        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        crop = crop_box(gray_screen, x, y, w, h)
        save_Path = f"{subfolder}/{name}.png"
        cv2.imwrite(save_Path, crop)
        print(f"{name} guardado como {name}.png")
