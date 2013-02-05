#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2006 Bermi Ferrer Martinez
# Copyright (c) 2006 Carles Sadurn\xed Anguita
#
# bermi a-t bermilabs - com
#
# See the end of this file for the free software, open source license (BSD-style).

import re
from .base import Base

class Spanish (Base):
    '''
    Inflector for pluralize and singularize Spanish nouns.
    '''
    
    def pluralize(self, word) :
        '''Pluralizes Spanish nouns.'''
        rules = [
            ['(?i)([aeiou])x$', '\\1x'], # This could fail if the word is oxytone.
            ['(?i)([\xe1\xe9\xed\xf3\xfa])([ns])$', '|1\\2es'],
            ['(?i)(^[bcdfghjklmn\xf1pqrstvwxyz]*)an$', '\\1anes'], # clan->clanes
            ['(?i)([\xe1\xe9\xed\xf3\xfa])s$', '|1ses'],
            ['(?i)(^[bcdfghjklmn\xf1pqrstvwxyz]*)([aeiou])([ns])$', '\\1\\2\\3es'], # tren->trenes
            ['(?i)([aeiou\xe1\xe9\xf3])$', '\\1s'], # casa->casas, padre->padres, pap\xe1->pap\xe1s
            ['(?i)([aeiou])s$', '\\1s'], # atlas->atlas, virus->virus, etc.
            ['(?i)([\xe9\xed])(s)$', '|1\\2es'], # ingl\xe9s->ingleses
            ['(?i)z$', 'ces'],  # luz->luces
            ['(?i)([\xed\xfa])$', '\\1es'], # ceut\xed->ceut\xedes, tab\xfa->tab\xfaes
            ['(?i)(ng|[wckgtp])$', '\\1s'], # Anglicismos como puenting, frac, crack, show (En que casos podr\xeda fallar esto?)
            ['(?i)$', 'es']	# ELSE +es (v.g. \xe1rbol->\xe1rboles)
        ]
        
        uncountable_words = ['tijeras','gafas', 'vacaciones','v\xedveres','d\xfaficit']
        ''' In fact these words have no singular form: you cannot say neither
        "una gafa" nor "un v\xedvere". So we should change the variable name to
        onlyplural or something alike.'''
        
        irregular_words = {
            'pa\xeds' : 'pa\xedses',
            'champ\xfa' : 'champ\xfas',
            'jersey' : 'jers\xe9is',
            'car\xe1cter' : 'caracteres',
            'esp\xe9cimen' : 'espec\xedmenes',
            'men\xfa' : 'men\xfas',
            'r\xe9gimen' : 'reg\xedmenes',
            'curriculum'  :  'curr\xedculos',
            'ultim\xe1tum'  :  'ultimatos',
            'memor\xe1ndum'  :  'memorandos',
            'refer\xe9ndum'  :  'referendos'
        }
        
        lower_cased_word = word.lower();
        
        for uncountable_word in uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word
        
        for irregular in list(irregular_words.keys()):
            match = re.search('(?i)('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)
        
        
        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            
            if match :
                groups = match.groups()
                replacement = rules[rule][1]
                if re.match('\|', replacement) :
                    for k in range(1, len(groups)) :
                        replacement = replacement.replace('|'+str(k), self.string_replace(groups[k-1], '\xc1\xc9\xcd\xd3\xda\xe1\xe9\xed\xf3\xfa', 'AEIOUaeiou'))
                
                result = re.sub(rules[rule][0], replacement, word)
                # Esto acentua los sustantivos que al pluralizarse se convierten en esdr\xfajulos como esm\xf3quines, j\xf3venes...
                match = re.search('(?i)([aeiou]).{1,3}([aeiou])nes$',result)
                
                if match and len(match.groups()) > 1 and not re.search('(?i)[\xe1\xe9\xed\xf3\xfa]', word) :
                    result = result.replace(match.group(0), self.string_replace(match.group(1), 'AEIOUaeiou', '\xc1\xc9\xcd\xd3\xda\xe1\xe9\xed\xf3\xfa') + match.group(0)[1:])
                    
                return result
        
        return word


    def singularize (self, word) :
        '''Singularizes Spanish nouns.'''
        
        rules = [
            ['(?i)^([bcdfghjklmn\xf1pqrstvwxyz]*)([aeiou])([ns])es$', '\\1\\2\\3'],
            ['(?i)([aeiou])([ns])es$',  '~1\\2'],
            ['(?i)oides$',  'oide'], # androides->androide
            ['(?i)(ces)$/i', 'z'],
            ['(?i)(sis|tis|xis)+$',  '\\1'], # crisis, apendicitis, praxis
            ['(?i)(\xe9)s$',  '\\1'], # beb\xe9s->beb\xe9
            ['(?i)([^e])s$',  '\\1'], # casas->casa
            ['(?i)([bcdfghjklmn\xf1prstvwxyz]{2,}e)s$', '\\1'], # cofres->cofre
            ['(?i)([gh\xf1pv]e)s$', '\\1'], # 24-01 llaves->llave
            ['(?i)es$', ''] # ELSE remove _es_  monitores->monitor
        ];
    
        uncountable_words = ['paraguas','tijeras', 'gafas', 'vacaciones', 'v\xedveres','lunes','martes','mi\xe9rcoles','jueves','viernes','cumplea\xf1os','virus','atlas','sms']
        
        irregular_words = {
            'jersey':'jers\xe9is',
            'esp\xe9cimen':'espec\xedmenes',
            'car\xe1cter':'caracteres',
            'r\xe9gimen':'reg\xedmenes',
            'men\xfa':'men\xfas',
            'r\xe9gimen':'reg\xedmenes',
            'curriculum' : 'curr\xedculos',
            'ultim\xe1tum' : 'ultimatos',
            'memor\xe1ndum' : 'memorandos',
            'refer\xe9ndum' : 'referendos',
            's\xe1ndwich' : 's\xe1ndwiches'
        }
    
        lower_cased_word = word.lower();
    
        for uncountable_word in uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word

        for irregular in list(irregular_words.keys()):
            match = re.search('('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)
            
        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            if match :
                groups = match.groups()
                replacement = rules[rule][1]
                if re.match('~', replacement) :
                    for k in range(1, len(groups)) :
                        replacement = replacement.replace('~'+str(k), self.string_replace(groups[k-1], 'AEIOUaeiou', '\xc1\xc9\xcd\xd3\xda\xe1\xe9\xed\xf3\xfa'))
                
                result = re.sub(rules[rule][0], replacement, word)
                # Esta es una posible soluci\xf3n para el problema de dobles acentos. Un poco guarrillo pero funciona
                match = re.search('(?i)([\xe1\xe9\xed\xf3\xfa]).*([\xe1\xe9\xed\xf3\xfa])',result)
                
                if match and len(match.groups()) > 1 and not re.search('(?i)[\xe1\xe9\xed\xf3\xfa]', word) :
                    result = self.string_replace(result, '\xc1\xc9\xcd\xd3\xda\xe1\xe9\xed\xf3\xfa', 'AEIOUaeiou')
                
                return result
        
        return word


# Copyright (c) 2006 Bermi Ferrer Martinez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.
