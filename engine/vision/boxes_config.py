# Diccionario anidado
class Box:
    def __init__(self, x, y, w, h):
        self.coords = (x, y, w, h)
        self.x, self.y, self.w, self.h = x, y, w, h

# --- VALORES GLOBALES DE AFINADO ---
X_1440, Y_1440, W_1440, H_1440 = 860, 650, 650, 30
X_1080, Y_1080, W_1080, H_1080 = 860, 650, 500, 25

BOXES_CONFIG = {
    1440: {
        "ROW0": {
            "COL0": Box(X_1440, Y_1440, W_1440, H_1440),
            "COL1": Box(X_1440, Y_1440, W_1440, H_1440),
            "COL2": Box(X_1440, Y_1440, W_1440, H_1440)
        },
        "ROW1": {
            "COL0": Box(X_1440, Y_1440, W_1440, H_1440),
            "COL1": Box(X_1440, Y_1440, W_1440, H_1440),
            "COL2": Box(X_1440, Y_1440, W_1440, H_1440)
        }
    },
    1080: {
        "ROW0": {
            "COL0": Box(X_1080, Y_1080, W_1440, H_1440),
            "COL1": Box(X_1080, Y_1080, W_1440, H_1440),
            "COL2": Box(X_1080, Y_1080, W_1440, H_1440)
        }
    }
}