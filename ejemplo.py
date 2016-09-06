#!/usr/bin/env python3

import legibilidad

TextoDePrueba = '''
Tuvo muchas veces competencia con el cura de su lugar (que era hombre docto graduado en Sigüenza), sobre cuál había sido mejor caballero, Palmerín de Inglaterra o Amadís de Gaula; mas maese Nicolás, barbero del mismo pueblo, decía que ninguno llegaba al caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.

En resolución, él se enfrascó tanto en su lectura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio, y así, del poco dormir y del mucho leer, se le secó el cerebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamientos, como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles, y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo.

'''

# Muestra la lecturabilidad
print(legibilidad.lecturabilidad(TextoDePrueba))

# Interpretación de la lecturabilidad

print(legibilidad.interpretaL(legibilidad.interpretaL(TextoDePrueba)))

# Muestra la perspicuidad
print(legibilidad.perspicuidad(TextoDePrueba))

# Interpretación de la perspicuidad

print(legibilidad.interpretaP(legibilidad.perspicuidad(TextoDePrueba)))
