# Legibilidad 2 (beta)
# Averigua la legibilidad de un texto
# Spanish readability calculations
# © 2016 Alejandro Muñoz Fernández

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




import re
import statistics


def count_letters(text):
    '''
    Text letter count
    '''
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    if count == 0:
        return 1
    else:
        return count

def letter_dict(text):
    '''
    letter count dictionary
    '''
    text = text.lower()
    replacements = {'á': 'a','é': 'e','í': 'i','ó': 'o','ú': 'u','ü': 'u'}
    for i, j in replacements.items():
        text = text.replace(i, j)
    letterlist = list(filter(None,map(lambda c: c if c.isalpha() else '', text)))
    letterdict = dict()
    for letter in letterlist:
        letterdict[letter] = letterdict.get(letter,0) + 1
    return letterdict


def count_words(text):
    '''
    Text word count
    '''
    text = ''.join(filter(lambda x: not x.isdigit(), text))
    clean = re.compile('\W+')
    text = clean.sub(' ', text).strip()
    # Prevents zero division
    if len(text.split()) == 0:
        return 1
    else:
        return len(text.split())


def textdict(wordlist):
    '''
    Dictionary of word counts
    '''
    wordlist = ''.join(filter(lambda x: not x.isdigit(), wordlist))
    clean = re.compile('\W+')
    wordlist = clean.sub(' ', wordlist).strip()
    wordlist = wordlist.split()
    # Word count dictionary
    worddict = dict()
    for word in wordlist:
        worddict[word.lower()] = worddict.get(word,0) + 1
    return worddict


def count_sentences(text):
    '''
    Sentence count
    '''
    text = text.replace("\n","")
    sentence_end = re.compile('[.:;!?\)\()]')
    sencences=sentence_end.split(text)
    sencences = list(filter(None, sencences))
    if len(sencences) == 0:
        return 1
    else:
        return len(sencences)

def count_paragraphs(text):
    '''
    Paragraph count
    '''
    text = re.sub('<[^>]*>', '', text)
    text = list(filter(None, text.split('\n')))
    if len(text) == 0:
        return 1
    else:
        return len(text)

def numbers2words(text):
    '''
    Comverts figures into words (e.g. 2 to two)
    '''
    import nal
    new_text = []
    for word in text.split():
        formato_numerico = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
        if re.match(formato_numerico,word):
            if type(word) == "int":
                word = int(word)
            else:
                word = float(word)
            word = nal.to_word(word)
        new_text.append(word.lower())
        
    text = ' '.join(new_text)
    return text


def count_syllables(word):
    '''
    Word syllable count
    '''
    import separasilabas
    word = re.sub(r'\W+', '', word)
    syllables = separasilabas.silabizer()
    return len(syllables(word))

def count_all_syllables(text):
    '''
    The whole text syllable count
    '''
    
    text = ''.join(filter(lambda x: not x.isdigit(), text))
    clean = re.compile('\W+')
    text = clean.sub(' ', text).strip()
    text = text.split()
    text = filter(None, text)
    total = 0
    for word in text:
        total += count_syllables(word)
    if total == 0:
        return 1
    else:
        return total

def Pval(text):
    '''
    Syllables-per-word mean (P value)
    '''
    syllables = count_all_syllables(numbers2words(text))
    words = count_words(numbers2words(text))
    return round(syllables / words,2)


def Fval(text):
    '''
    Words-per-sentence mean (F value)
    '''
    sencences = count_sentences(text)
    words = count_words(numbers2words(text))
    return round(words / sencences,2)


def fernandez_huerta(text):
    '''
    Fernández Huerta readability score
    '''
    fernandez_huerta = 206.84 - 60*Pval(text) - 1.02*Fval(text)
    return round(fernandez_huerta,2)


def szigriszt_pazos(text):
    '''
    Szigriszt Pazos readability score (1992)
    '''
    return round(206.835 - 62.3 * ( count_all_syllables(numbers2words(text)) / count_words(numbers2words(text))) - (count_words(numbers2words(text)) / count_sentences(text)),2)


def gutierrez(text):
    '''
    Gutiérrez de Polini's readability score (1972)
    '''
    legibguti = 95.2 - 9.7 * (count_letters(text) / count_words(text)) - 0.35 * (count_words(text) / count_sentences(text))
    
    return round(legibguti, 2)

def mu(text):
    '''
    Muñoz Baquedano and Muñoz Urra's readability score (2006)
    '''
    n = count_words(text)
    # Delete all digits
    text = ''.join(filter(lambda x: not x.isdigit(), text))
    # Cleans it all
    clean = re.compile('\W+')
    text = clean.sub(' ', text).strip()
    text = text.split() # word list
    word_lengths = []
    for word in text:
        word_lengths.append(len(word))
    # The mean calculation needs at least 1 value on the list, and the variance, two. If somebody enters only one word or, what is worse, a figure, the calculation breaks, so this is a 'fix'
    try:
        mean = statistics.mean(word_lengths)
        variance = statistics.variance(word_lengths)
        mu = (n / (n - 1)) * (mean / variance) * 100
        return round(mu, 2)
    except:
        return 0
    
    
def crawford(text):
    '''
    Crawford's readability formula
    '''
    sentences = count_sentences(text)
    words = count_words(numbers2words(text))
    syllables = count_all_syllables(numbers2words(text))
    SeW = 100 * sentences / words # number of sentences per 100 words (mean)
    SiW = 100 * syllables / words # number of syllables in 100 words (mean)
    years = -0.205 * SeW + 0.049 * SiW - 3.407
    years = round(years,1)
    return years


def interpretaP(P):
    '''
    Szigriszt-Pazos score interpretation
    '''
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
        return "muy fácil"
    
    
    
# Interpreta la fernandez_huerta
def interpretaL(L):
    if L < 30:
        return "muy difícil"
    elif L >= 30 and L < 50:
        return "difícil"
    elif L >= 50 and L < 60:
        return "bastante difícil"
    elif L >= 60 and L < 70:
        return "normal"
    elif L >= 70 and L < 80:
        return "bastante fácil"
    elif L >= 80 and L < 90:
        return "fácil"
    else:
        return "muy fácil"
    
    
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
    

def gutierrez_interpret(G):
    if G <= 33.33:
        return "difícil"
    if G > 33.33 and G < 66.66:
        return "normal"
    else:
        return "fácil"
    
def mu_interpret(M):
    if M < 31:
        return "muy difícil"
    elif M >= 31 and M <= 51:
        return "difícil"
    elif M >= 51 and M < 61:
        return "un poco difícil"
    elif M >= 61 and M < 71:
        return "adecuado"
    elif M >= 71 and M < 81:
        return "un poco fácil"
    elif M >= 81 and M < 91:
        return "fácil"
    else:
        return "muy fácil"

# See ejemplo.py to see how it works!
