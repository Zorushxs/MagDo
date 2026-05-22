import ctypes
from ctypes import wintypes

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
    ]


def monitor_details(indice_monitor):

    # 1. Avisar a Windows que queremos los píxeles reales
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    user32 = ctypes.windll.user32
    shcore = ctypes.windll.shcore
    monitores = []

    # Callback para encontrar los "Handles" (identificadores únicos) de cada monitor
    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        # Se inicializa el constructor
        info = MONITORINFO()
        # Se asigna la longitud de la estructura de datos para C
        info.cbSize = ctypes.sizeof(MONITORINFO)

        # Revisa si hay datos usables
        if user32.GetMonitorInfoW(hMonitor, ctypes.byref(info)):
            # Guardamos el identificador (hMonitor) y sus coordenadas
            monitores.append({
                "handle": hMonitor,
                "rect": info.rcMonitor
            })
        return True

    # Contrato de Traducción, se define cómo deben comunicarse los bits entre Python y Windows
    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
    user32.EnumDisplayMonitors(None, None, CMPFUNC(callback), 0)

    #print(f"{monitores}")

    if 0 <= indice_monitor < len(monitores):
        monitor = monitores[indice_monitor]

        # --- CÁLCULO DE RESOLUCIÓN ---
        ancho_real = monitor["rect"].right - monitor["rect"].left
        alto_real = monitor["rect"].bottom - monitor["rect"].top

        # --- CÁLCULO DE ESCALA (DPI) ---
        # Usamos el 'handle' específico de ese monitor
        escala = ctypes.c_uint()
        shcore.GetScaleFactorForMonitor(monitor["handle"], ctypes.byref(escala))

        factor = escala.value

        return {
            "monitor_id": indice_monitor,
            "ancho_físico": ancho_real,
            "alto_físico": alto_real,
            "escala": factor,
            "ancho_lógico": int(ancho_real / (factor / 100)),
            "alto_lógico": int(alto_real / (factor / 100))
        }
    else:
        raise IndexError(f"Monitor con índice {indice_monitor} no encontrado. Detectados: {len(monitores)}")

# --- Uso del script ---
#   try:
#       indice_monitor = 1;
#       monitor = obtener_detalles_monitor(indice_monitor) # '1' para el segundo monitor
#
#       if monitor:
#           print(f"Monitor {monitor['monitor_id']} - Escala: {monitor['escala']}%")
#           print(f"Físico: {monitor['ancho_físico']}x{monitor['alto_físico']}")
#           print(f"Lógico: {monitor['ancho_lógico']}x{monitor['alto_lógico']}")
#   except IndexError as e:
#       print(e)