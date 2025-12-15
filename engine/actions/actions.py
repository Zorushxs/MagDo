# script encargado de interactuar con la aplicación según dicte el script de lógica

# Según imagino en este script (o quizás habría que definir algunos scripts más para que quedara de forma modular),
# se crearían distintas acciones para cada uno de las órdenes posibles dictadas por la lógica.
# Como meter algún tipo de runa -> aunque pensándolo bien debería ser más tipo mete runa de este row, y diferenciar por row
# Sí, pero identificar que tipo de atributo es el row, esa info extra me puede ayudar. Quizás para facilitar la cosa de
# en que row se encuentra cada atributo, guardar inicialmente cuantas rows hay con qué atributo cada una y trabajar con
# este set de datos, asi no hay que hacer comprobaciones tediosas al principio iterativas, no está exempto, pero me huelo
# que serán más simples.

# También habría que tener en cuenta que cada vez que se mete algo exo todo se corre una linea más a bajo, y si desaparece hacia arriba

# Crear una funcion para clickar en una área determinada de forma estadística para evitar ser detectado como máquina,
# en esta funcion se haría un gradiente sobre una parte del área determinada, asi como el tiempo en el que se acciona
# la accion para que no sean acciones periódicas. Debe ser un tiempo creíblemente humano.