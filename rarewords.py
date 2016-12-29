#!/usr/bin/env python3

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

import sqlite3

def rare_words(wordlist):
    '''
    List of rare words (not in the SUBTLEX-ESP database). Fix this: make only one query instead of one per word. It'll be faster
    '''
    dbpath = "/home/protected/db/SUBTLEX-ESP.db"
    
    conn = sqlite3.connect(dbpath)
    rarewords = []
    cur = conn.cursor()
    for word in wordlist:
        cur.execute('SELECT 1 FROM frecuencias WHERE palabra = ? LIMIT 1', (word,))
        if not cur.fetchone():
            rarewords.append(word)
    conn.close()
    return rarewords