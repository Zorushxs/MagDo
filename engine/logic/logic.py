# script encargado de tomar decisiones según la interpretación de los datos de las capturas de pantalla

# Creo que o deberia crearse un espacio de memoria aparte o en lógica para retener la información obtenida por ocr
# Se me ocurren varios modos:
# - Crear un módulo más de full datos
# - Integrar el primer punto en el script ocr, en vez de ser uno própio
# - Este me gusta algo más, que sea algo dinámico, me explico, que sea por ejemplo una array que su ciclo de vida sea
#   una iteración de la lógica. Y que después se borre/sobreescriba. Me parece más guay, ya que está pensado un sistema
#   de logs que permitirá seguir el flujo. Este bloque de logs, tengo en mente que sea bastante útil para depurar y
#   mejorar la lógica, por lo tanto será agradable de leer e irá acompañado de bastantes datos, la imagen a procesar,
#   los datos interpretados a través de la imagen, y más cosas que puedan valor que se me ocurran.

# Deberia mediante los datos guardados u obtenidos en memoria saber los límites de los stats del ítem y según las
# preferencias introducidas proceder a dar órdenes de una accion u otra al script de actions