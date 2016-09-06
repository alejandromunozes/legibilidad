# Legibilidad. 0.1 (beta)
# Averigua la legibilidad de un texto
# 2016 Alejandro Muñoz Fernández

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


###Cálculo de la lecturabilidad con la fórmula de Fernández-Huerta (1959)
# Lecturabilidad = 206,84 – 0,60 P – 1,02 F
# P = número de sílabas por cada cien palabras
# F = número de frases por cada cien palabras

### Cálculo de la perspicuidad de Szigriszt-Pazos (1993)
# Perspicuidad = 206.835 – 62.3 (S/P – P/F)
# P = palabras totales
# S = silabas totales
# F = frases totales

import re

# Contar palabras

def contar_palabras(texto):
    texto = ''.join(filter(lambda x: not x.isdigit(), texto))
    limpia = re.compile('\W+')
    texto = limpia.sub(' ', texto).strip()
    return len(texto.split())

# Contar frases

def contar_frases(texto):
    texto = texto.replace("\n","")
    FinDeFrase = re.compile('[.:;¡!¿?\)\()]')
    frases=FinDeFrase.split(texto)
    frases = list(filter(None, frases))
    return len(frases)

# Convierte las cifras de los números de un texto a letras (p.ej. :21 a veintiuno)

def cifras_a_letras(texto):
    import nal
    textonuevo = []
    for palabra in texto.split():
        formato_numerico = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
        if re.match(formato_numerico,palabra):
            if type(palabra) == "int":
                palabra = int(palabra)
            else:
                palabra = float(palabra)
            palabra = nal.to_word(palabra)
        textonuevo.append(palabra)
        
    texto = ' '.join(textonuevo)
    return texto


# Cuenta las sílabas de una palabra
import separasilabas
def contar_silabas(palabra):
    palabra = re.sub(r'\W+', '', palabra)
    silabas = separasilabas.silabizer()
    return len(silabas(palabra))
    

# Cuenta las sílabas de todas las palabras

def contar_total_silabas(texto):
    
    texto = ''.join(filter(lambda x: not x.isdigit(), texto))
    limpia = re.compile('\W+')
    texto = limpia.sub(' ', texto).strip()
    texto = texto.split()
    texto = filter(None, texto)
    total = 0
    for palabra in texto:
        total += contar_silabas(palabra)
    return total


# Valor P. Promedio de sílabas por cada cien palabras

def valorP(texto):
    silabas = contar_total_silabas(cifras_a_letras(texto))
    palabras = contar_palabras(cifras_a_letras(texto))
    return round(silabas / palabras,2)


# Valor F. Promedio de frases por cada cien palabras

def valorF(texto):
    frases = contar_frases(texto)
    palabras = contar_palabras(cifras_a_letras(texto))
    return round(palabras / frases,2)

# Lecturabilidad

def lecturabilidad(texto):
    lecturabilidad = 206.84 - 60*valorP(texto) - 1.02*valorF(texto)
    return round(lecturabilidad,2)

# Interpreta la lecturabilidad
def interpretaL(L):
    if L < 30:
        return "muy difícil"
    elif L >= 30 and L < 50:
        return "difícil"
    elif L >= 50 and L < 60:
        return "bastante difícil"
    elif L >= 60 and L < 70:
        return "normal para un adulto"
    elif L >= 70 and L < 80:
        return "bastante fácil"
    elif L >= 80 and L < 90:
        return "fácil"
    else:
        return "muy fácil"

# Perspicuidad

def perspicuidad(texto):
    return round(206.835 - 62.3 * ( contar_total_silabas(cifras_a_letras(texto)) / contar_palabras(cifras_a_letras(texto))) - (contar_palabras(cifras_a_letras(texto)) / contar_frases(texto)),2)

# Interpreta la perspicuidad

def interpretaP(P):
    if P <= 15:
        return "muy difícil"
    elif P > 15 and P <= 35:
        return "árido"
    elif P > 35 and P <= 50:
        return "bastante difícil"
    elif P > 50 and P <= 65:
        return "normal"
    elif P > 65 and P <= 75:
        return "bastante fácil"
    elif P > 75 and P <= 85:
        return "fácil"
    else:
        return "fácil"
    
# Interpretación Inflesz

def inflesz(P):
    if P <= 40:
        return "muy difícil"
    elif P > 40 and P <= 55:
        return "algo difícil"
    elif P > 55 and P <= 65:
        return "normal"
    elif P > 65 and P <= 80:
        return "bastante fácil"
    else:
        return "muy fácil"
