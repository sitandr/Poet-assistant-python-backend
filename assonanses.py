import numpy as np
import yaml
import re

TRASCRIPT_CONFIG = yaml.safe_load(open('convertation.yaml',
                                       encoding = 'utf-8'))

GROUPS = list(TRASCRIPT_CONFIG['groups'].keys()) # this assumes that the order is important; however, python dicts don't
# gurantee it, so it shold be replaced (but it works)

J_VOWELS_JOTTED = [' ', 'ъ', 'ь'] + list(TRASCRIPT_CONFIG['assonance_vectors'].keys())
GROUP_STRUCTURE = {TRASCRIPT_CONFIG['groups'][group][group_number]: (group, group_number)
                   for group in TRASCRIPT_CONFIG['groups']
                   for group_number in range(len(TRASCRIPT_CONFIG['groups'][group]))}

BASIC_VOWELS = TRASCRIPT_CONFIG['assonance_vectors'].keys()

import string
SONOT_OFF_REGEX = re.compile("\*[ $" + re.escape(string.punctuation) + "]")

import pprint
pprint.pprint(TRASCRIPT_CONFIG)

### global

def is_item_vowel(item): # also works for letter because 'l'[0] == 'l'
    return item[0] in BASIC_VOWELS

def assonance_closeness(v1, v2):
    v1 = TRASCRIPT_CONFIG['assonance_vectors'][v1]
    v2 = TRASCRIPT_CONFIG['assonance_vectors'][v2]
    
    return (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2

### final_check

def check(w1, w2):
    print(w1, w2)
    w1 = reversed_transcription_to_array(transcript(w1))
    w2 = reversed_transcription_to_array(transcript(w2))

    w1 = vowel_split(w1)
    w2 = vowel_split(w2)
    
    end_remains_1 = not is_item_vowel(w1[0][0])
    end_remains_2 = not is_item_vowel(w2[0][0])


    sim = (end_remains_1 == end_remains_2)*10
    for i in range(min(len(w1) - end_remains_1,
                       len(w2) - end_remains_2)):
        i1 = w1[i + end_remains_1]
        i2 = w2[i + end_remains_2]
        stress1 = '.' if len(i1) == 1 else i1[1]
        stress2 = '.' if len(i2) == 1 else i2[1]
        stresses = sorted((p1, p2))
        
        if stresses == ["'", '.']: # strict and not strict stress
            return 0 # bad rythm
        
        point_closeness = assonance_closeness(i1[0], id2[0])
        
        if stresses == ["'", "`"]:
            point_closeness *= 2

        if stresses == ["'", "'"]:
            point_closeness *= 5
        
        sim -= point_closeness

    for i in range(len(w1)):
        ...



def letter_similarity(l1, l2):
    sim = 0
    if l1[0] != l2[0]:
        # 2.25 max
        return (4 - abs(GROUPS.index(l1[0][0]) - GROUPS.index(l2[0][0])))**2/4

    assert len(l1[0]) == len(l2[0])
    
    if len(l1[0]) > 1: # has num
        sim += 20/(1 + abs(int(l1[0][1]) - int(l2[0][1])))
    else:
        sim += 20
    
    sim += 6 - 3*(len(set(l1[1:]) ^ set(l2[1:])))
    return sim # 26 max



### arrayisation

def reversed_transcription_to_array(w):
    word = []
    temp = []
    num = None
    for lett in w:
        if lett in "'`*":
            temp.append(lett)
        elif lett in ''.join(map(str, range(10))):
            num = (lett)
        else:
            if num:
                lett += num
                num = None
            word.append([lett] + temp[::-1])
            temp = []
    return word

def vowel_split(array):
    word = []
    syllable = [] # starts with vowel
    
    for item in array:
        if is_item_vowel(item[0]): # vowel
            if syllable:
                word.append(syllable)
                syllable = []
            
            syllable = [item]
            continue
        syllable.append(item)
        
    word.append(syllable)

    return word    

### transcription

def transcript(w):
    w = j_vowels_replace(w)
    w = primary_replace(w)
    w = group_replace(w)
    w = secondary_replace(w)
    w = w[::-1]
    
    return w

def j_vowels_replace(w):
    
    for lett in TRASCRIPT_CONFIG['j_vowel']:
        
        replace_to = TRASCRIPT_CONFIG['j_vowel'][lett]
        
        while True:
            ind = w.find(lett)
            
            if ind == -1:
                break

            if ind == 0 or w[ind - 1] in J_VOWELS_JOTTED:
                w = w[:ind - 1] + 'j' + replace_to + w[ind + 1:]
            else:
                w = w[:ind] + '`' + replace_to + w[ind + 1:]

    return w
            
def primary_replace(w):
    for l in TRASCRIPT_CONFIG['replace']:
        w = w.replace(l, TRASCRIPT_CONFIG['replace'][l])
    return w

def letter_group_convert(l):
    if l not in GROUP_STRUCTURE:
        # print(l)
        return l
    return ''.join(map(str, GROUP_STRUCTURE[l]))

def group_replace(w):
    "Replace consonants with their numbers and groups"
    letters = list(w)
    letters = map(letter_group_convert, letters)
    letters = ''.join(letters)
    return ''.join(letters)

def secondary_replace(w):
    "More complicated final replace logic"

    finder = re.finditer(SONOT_OFF_REGEX, w) # remove * if end of the word
    for match in finder:
        w = w[:match.start()] + w[match.start() + 1:]
        
    # BUG -> FEATURE: this also works for ` due to "punctuation" in regexp
    
    w = w.replace(' ', '')
        
    return w

w1 = "бро'шу"
w2 = "хоро'ший"
w3 = "галью'н"
w4 = "лягу'шка"
w5 = "коль ты'"
w6 = "ца'пля"
w7 = "лё'д"
w8 = "дро'бь"

check(w1, w2)
check(w1, w3)
check(w1, w4)
check(w1, w5)
check(w1, w6)
check(w1, w7)
check(w1, w8)
check("сла'ва", "сле'ва")

# import pickle
# a = pickle.load(open('normal_stresses.pkl', 'rb'))
