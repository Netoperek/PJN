#!/usr/bin/env/python
# -*- coding: utf-8 -*- 
from plp import PLP
import sys
import re
p = PLP()

def parse_input(file, split_sign):
    sentences = []
    f = open(file)
    for line in f:
        line = re.sub("\n", '', line)
        sentences.append(line.split(split_sign))
    return sentences

def to_simple_form(sentences):
    simple_sentences = []
    for sentence in sentences:
        simple_words = []
        for word in sentence:
            id = p.rec(word.decode('UTF-8'))
            if(len(id) > 0):
                simple_word = p.bform(id[0])
                simple_words.append(simple_word)
        simple_sentences.append(simple_words)
    return simple_sentences

def carthesian_mul(words):
    pairs = []
    for i in xrange(len(words)):
        for j in range(i+1, len(words)):
            pairs.append([words[i], words[j]])

    return pairs

def compare_pairs(pairs1, pairs2):
    matched_pairs = []
    for ele in pairs1:
        unicode_ele = []
        for e in ele:
           unicode_ele.append(e.decode('UTF-8')) 
        for ele2 in pairs2:
            if unicode_ele == ele2 or unicode_ele[::-1] == ele2:
                matched_pairs.append(unicode_ele)
    return matched_pairs

def prettify_pairs(pairs, weight_dict):
    string_pairs = "" 
    for pair in pairs: 
        string_pairs += "(" + pair[0] + "," + pair[1] + "[" + str(weight_dict[pair[1]]) + "]" ")"
    return string_pairs

def weight_dict(pairs):
    dict = {}
    for pair in pairs:
        dict[pair[1].decode('utf-8')] = int(pair[0])
    return dict

sentences = parse_input('out',' ')
simple_sentences = to_simple_form(sentences)

pairs1 = parse_input('mleko_pairs.csv',',')
weights = parse_input('mleko_wagi.csv',',')
weight_dict = weight_dict(weights)

winners = []
loosers = []

for i in xrange(len(simple_sentences)):
    simple_sentence = simple_sentences[i]
    sentence = sentences[i]
    pairs2 = carthesian_mul(simple_sentence)
    matched_pairs = compare_pairs(pairs1, pairs2)
    if(len(matched_pairs) > 0):
        winners.append(sentence)
        winners.append(prettify_pairs(matched_pairs, weight_dict))
        winners.append("")
    else:
        loosers.append(sentence)

for win in winners:
    print " ".join(win)
#print ""
#print "LOSERS"
#print ""
#for looser in loosers:
#    print " ".join(looser)

print len(winners) / 3
