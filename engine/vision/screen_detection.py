import ctypes

def configurar_dpi():
    """Avisa a Windows que use píxeles reales para evitar desenfoque."""
    try:
        # Intentamos usar shcore (Win 8.1+)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        # Fallback para sistemas más antiguos (Win 7/8)
        ctypes.windll.user32.SetProcessDPIAware()

def obtener_datos_pantalla():

    configurar_dpi()

    # 1. Avisar a Windows que queremos los píxeles reales (DPI Aware)
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    user32 = ctypes.windll.user32

    # 2. Obtener resolución física real (píxeles totales del panel)
    ancho_real = user32.GetSystemMetrics(0)
    alto_real = user32.GetSystemMetrics(1)

    # 3. Obtener el factor de escala (ej: 125 para 125%)
    escala = ctypes.windll.shcore.GetScaleFactorForDevice(0)

    # 4. Calcular resolución lógica (la que verías sin escalado)
    ancho_logico = int(ancho_real / (escala / 100))
    alto_logico = int(alto_real / (escala / 100))

    print(f"Resolución Física: {ancho_real}x{alto_real}")
    print(f"Escalado: {escala}%")
    print(f"Resolución Lógica: {ancho_logico}x{alto_logico}")

obtener_datos_pantalla()