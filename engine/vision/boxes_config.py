# Diccionario anidado
class Box:
    def __init__(self, x, y, w, h):
        self.coords = (x, y, w, h)
        self.x, self.y, self.w, self.h = x, y, w, h

# Configuración por columna: (X, Offset_Ancho)
COLS_DATA = [
    (860, 0),    # COL0
    (935, 0),    # COL1
    (1033, 148), # COL2
    (1251, 0),   # COL3
    (1350, - 22), # COL4
    (1398, - 28), # COL5
    (1440, - 28)  # COL6
]

Y_BASE, W_BASE, H_BASE = 480, 70, 32
Y_STEP = 45

def generate_row_with_cols(row_idx):
    y = Y_BASE + (row_idx * Y_STEP)
    return {
        f"COL{i}": Box(x, y, W_BASE + w_off, H_BASE)
        for i, (x, w_off) in enumerate(COLS_DATA)
    }

BOXES_CONFIG = {
    1440: {
        f"ROW{r}": generate_row_with_cols(r) for r in range(14)
    },
    1080: {
        # Aquí puedes añadir la lógica para 1080 de forma similar
    }
}
