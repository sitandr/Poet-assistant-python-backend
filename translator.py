import yaml
import re

import utils

TRASCRIPT_CONFIG = yaml.safe_load(open('convertation.yaml',
                                       encoding = 'utf-8'))

GROUPS = list(TRASCRIPT_CONFIG['groups'].keys()) # this assumes that the order is important; however, python dicts don't
# gurantee it, so it could be be replaced (but it works for Python >= 3.7)

J_VOWELS_JOTTED = ([' ', 'ъ', 'ь', "'"] + list(TRASCRIPT_CONFIG['assonance_vectors'].keys())+
                   list(TRASCRIPT_CONFIG['j_vowel'].keys()))

GROUP_STRUCTURE = {TRASCRIPT_CONFIG['groups'][group][group_number]: (group, group_number)
                   for group in TRASCRIPT_CONFIG['groups']
                   for group_number in range(len(TRASCRIPT_CONFIG['groups'][group]))}

BASIC_VOWELS = TRASCRIPT_CONFIG['assonance_vectors'].keys()

import string
SONOT_OFF_REGEX = re.compile("\*([ " +
                             '!"\\#\\$%\\&\'\\(\\)\\*\\+,\\-\\./:;<=>\\?@\\[\\\\\\]\\^_\\{\\|\\}\\~'
                             + "]|$)")

#import pprint
#pprint.pprint(TRASCRIPT_CONFIG)

### global

def is_item_vowel(item): # also works for letter because 'l'[0] == 'l'
    return item[0] in BASIC_VOWELS

def assonance_distance(v1, v2):
    # just not jotted letters, stresses should be treated at higher level
    v1 = TRASCRIPT_CONFIG['assonance_vectors'][v1]
    v2 = TRASCRIPT_CONFIG['assonance_vectors'][v2]
    
    return (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2

def alliteration_similarity(l1, l2):
    # complex objects
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


### final_check


def check(w1, w2):

    # utils.timer('s')
    w1 = full_transcript(w1)
    # utils.timer('w1')
    w2 = full_transcript(w2)
    # utils.timer('w2')
    res = transcripted_check(w1, w2)
    # utils.timer('tc')
    return res

def transcripted_check(w1, w2):
    k_consend = 0.05
    k_assonanses = 1/5

    end_remains_1 = not is_item_vowel(w1[0][0]) # is there a consonant(s) in the end of first world 
    end_remains_2 = not is_item_vowel(w2[0][0]) # …of the second world

    sim = (end_remains_1 == end_remains_2)*k_consend
                    
    allit_sim = vowel_ryphm_component(w1, w2, end_remains_1, end_remains_2)
    assonance_sim = assonance_ryphm_component(w1, w2, end_remains_1, end_remains_2)
    return (sim + allit_sim
            + assonance_sim*k_assonanses)

def vowel_ryphm_component(w1, w2, end_remains_1, end_remains_2,
                          k_not_strict_stress = 5, k_strict_stress = 20):
    allit_sim = 0
    # check of vowels sounds
    for syll in range(min(len(w1) - end_remains_1,
                       len(w2) - end_remains_2)):
        # syll is number of current syllable (starts with vowel in back notation) without consonant-end
        
        i1 = w1[syll + end_remains_1][0] # vowels of syllable
        i2 = w2[syll + end_remains_2][0]
        stress1 = '.' if len(i1) == 1 else i1[1]
        stress2 = '.' if len(i2) == 1 else i2[1]
        stresses = sorted((stress1, stress2))
        
        if stresses == ["'", '.']: # strict and strict no stress
            return -100 # bad rythm
       
        vowel_dist = assonance_distance(i1[0], i2[0])
        
        if stresses == ["'", "`"]:
            vowel_dist *= k_not_strict_stress

        if stresses == ["'", "'"]:
            vowel_dist *= k_strict_stress
        
        allit_sim -= vowel_dist
    return allit_sim/(len(w1) + len(w2))

def assonance_ryphm_component(w1, w2, end_remains_1, end_remains_2,
                              shift_coord_assonanse = 1.0, shift_syll_ending = 1.0,
                              pow_coord_delta = 3, pow_syll_ending = 1):
    assonance_sim = 0
    i = 0
    # terrible nesting, but have no idea how to make it better
    for syll1 in range(len(w1)):
        
        # temporaly remove vowel 
        syll_data1 = w1[syll1][1:] if (not end_remains_1 or syll1 != 0) else w1[syll1]
        for lett1 in range(len(syll_data1)):
            for syll2 in range(len(w2)):
                syll_data2 = w2[syll2][1:] if (not end_remains_2 or syll2 != 0) else w2[syll2]
                for lett2 in range(len(syll_data2)):

                    coord_distance = ((syll2 - syll1 + end_remains_1 - end_remains_2) +
                                      (lett2 - lett1)/(len(syll_data2) + len(syll_data1)))
                    
                    # second summand ×2 for more correct distance, but this is better because letter dist
                    # "weights" less; in fact, there is just a coefficient 2
                    
                    value_sim = alliteration_similarity(syll_data1[lett1], syll_data2[lett2])
                    
                    assonance_sim += (value_sim/(abs(coord_distance) + shift_coord_assonanse)**pow_coord_delta
                                      /(syll1 + syll2 + shift_syll_ending)**pow_syll_ending)
                    i += 1
                    
    return assonance_sim/(i + 1)

def full_transcript(w):
    w = transcript(w)
    w = reversed_transcription_to_array(w)
    w = vowel_split(w)
    return w

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

            if ind == 0: # start of the word
                w = 'j' + replace_to + w[1:]
            elif w[ind - 1] in J_VOWELS_JOTTED: # j should appear
                w = w[:ind] + 'j' + replace_to + w[ind + 1:]
            else: # just make previous sound softened (?)
                w = w[:ind] + '`' + replace_to + w[ind + 1:]

    return w
            
def primary_replace(w):
    for l in TRASCRIPT_CONFIG['replace']:
        w = w.replace(l, TRASCRIPT_CONFIG['replace'][l])
    return w

def letter_group_convert(l):
    if l not in GROUP_STRUCTURE:
        return l # vowel
    
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
    res = ''
    pr = 0
    for match in finder:
        res += w[pr:match.start()]
        pr = match.start() + 1
    res += w[pr:]
        
    # BUG -> FEATURE: this also works for ` due to "punctuation" in regexp
    
    res = res.replace(' ', '')
        
    return res

##w1 = "бро'шу"
##w2 = "хоро'ший"
##w3 = "галью'н"
##w4 = "лягу'шка"
##w5 = "коль ты'"
##w6 = "ца'пля"
##w7 = "лё'д"
##w8 = "дро'бь"
##
##check(w1, w2)
##check(w1, w3)
##check(w1, w4)
##check(w1, w5)
##check(w1, w6)
##check(w1, w7)
##check(w1, w8)
##check("сла'ва", "сле'ва")

# import pickle
# a = pickle.load(open('normal_stresses.pkl', 'rb'))
# check("куса'ть", "еванге'лик")
