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

#  leer estado (interpretacion de la lectura, minimos y maximos y entender como se encuentran los stats del objeto)
#  guardar variables para saber que arreglar e irlas actualizando
#  bucle iterativo
#  	ver que tiene más prioridad a la hora de querer arreglar
#  		aquí es donde, si se usa, se deben usar los restos para calcular cuanto puede "petar" el objeto
#  		para saber que tiene más prioridad usar variable que defina que cuál es el stat sobre el que quieres actuar
#  		aquí hay que codificar que si se cumplen las condiciones requeridas no hace falta seguir -> usar el booleano
#  	    mandar la orden de arreglar lo que tiene más prioridad
#  	actualizar estados para saber como proceder en la siguiente iteracion
#  		entre ellos la variable que define el stat sobre el que quieres actuar
#  		otra variable a actualizar es el tier de la runa, evaluar cuál meter según el valor actual y el rango.
#  		los restos

# a ver como creo el metodo y la estructura de datos que contendrá la información para actuar sobre dofus para subir el stat.
# opcion 1
#   metodo:
#       este metodo recibira un stat como "fuerza" y sabrá en que row está, porque durante la lectura se habrá actualizado
#       la estructura de datos con los datos leidos con ocr.
#       Con esta info podra realizar la accion pedida. Aquí metera runas tier 1, 2 o 3 según o se le defina en la
#       entrada o puedo hacer que se defina aquí dentro. Debido a que es un script de actuacion, sería más lógico que
#       venga definido en la entrada el tier de la runa.
#   estructura de datos:
#       set tipo
#           stat "fuerza"
#           row "1"
#           tier runa "2"
#       set exo tipo
#           stat "PA"
#           row "0" al principio no habrá valor, pero si entra en la lectura se seteará y modificará el booleano de parar magueo
#           tier runa "1" podrá ser cualquiera pero la gran mayoria de veces será 1
#   stat que quiero actualizar
#   restos
#   booleano para definir si se sigue o no magueando
