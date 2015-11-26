#!/usr/bin/env/python
# -*- coding: utf-8 -*- 
from plp import PLP
import sys
import re
p = PLP()

IS_VERB = u'być'

LIMIT = 50
EXCLUDE_VEC = [1, 13, 14, 45, 46, 47]
EXLCUDE_WORDS = ['wiadomo']

def parse_input(file):
    words = []
    f = open(file)
    for line in f:
        line = re.sub('[,.\-()"]', '', line)
        search_word = re.search('\w+', line)
        if(search_word != None):
            line = line.split()
            line.append('\n')
            words.append(line)
    return words


def get_word_indices(stimulus, line):
    stimulus_indicies = []
    for i in range(len(line)):
        if line[i].decode('utf-8').lower() in p.forms(p.rec(stimulus)[0]):
            stimulus_indicies.append(i)
    return stimulus_indicies

def border_ok(word_rec, word):
    if(p.label(word_rec)[0] != PLP.CZESCI_MOWY.CZASOWNIK):
        return False
    if(p.bform(word_rec) == IS_VERB):
        return False
    if(p.vec(word_rec, word)[0] in EXCLUDE_VEC):
        return False 
    if(word in EXLCUDE_WORDS):
        return False 

    return True

def extract_snippet(indices, line):
    result = []
    sentences = []
    left_border_found = False
    right_border_found = False
    for i in indices:
        j = i - 1
        left = i
        right = i
        list = []
        while True:
            if(j >= 0 and i - j <= LIMIT):
                word = line[j].decode('utf-8') 
                word_rec = p.rec(word)
                if(len(word_rec) > 0):
                    word_rec = word_rec[0]
                    if(border_ok(word_rec, word)):
                        left_border_found = True
                        left = j
                        break
            else:
                break
            j = j - 1

        j = i + 1
        while True:
            if(j - i <= LIMIT and j < len(line)):
                word = line[j].decode('utf-8') 
                word_rec = p.rec(word)
                if(len(word_rec) > 0):
                    word_rec = word_rec[0]
                    if(border_ok(word_rec, word)):
                        right_border_found = True
                        right = j
                        break
            else:
                break
            j = j + 1

        for i in xrange(left, right + 1):
            list.append(line[i])
        result.append(list)

    if(not left_border_found or not right_border_found):
        return []

    for list in result:
       sentences.append(" ".join(list))
    return sentences

lines = parse_input('mleko')
result = []
for line in lines:
    indices = get_word_indices('mleko', line)
    sentences = extract_snippet(indices, line)
    result.extend(sentences)

result = list(set(result))
index = 0

for ele in result:
    index = index + 1
    print ele
