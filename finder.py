from translator import check, full_transcript, transcripted_check

import utils

import wv
import bisect

from coefficients import k_meaning
import coefficients
from resource_importer import words_loaded, special_info

def getstressed(word):
      res = words[word][0]
      if res == '-':
            return words[word][1]
      return res

def normalize(word):
      return word.replace('`', '').replace("'", '')



normal_forms = list(words_loaded.keys())

def get_all_forms_of(elements, words = None):
      if not words: words = words_loaded
      no_change = ['?', 'част', 'союз', 'н', 'межд', 'вводн']
      
      if elements[0] in no_change or elements[-1] == ['']:
            yield elements[1]
            return
      
      ps = elements[-1].split(';')
      for p in ps:
            if p and p[0].isdigit():
                  yield elements[1 + int(p[0])] + p[1:]
            else:
                  yield elements[1] + p

def get_best_form(elements, to_find_data, words = None):
      if not words: words = words_loaded
      
      best = float('-inf')
      best_form = None
      for form in get_all_forms_of(elements, words):
            new = transcripted_check(to_find_data, full_transcript(form))
            if new > best:
                  best = new
                  best_form = form
      return best, best_form

def get_best_by_transcription(to_find,
                              remove = [],
                              words = None,
                              n_best = 500,
                              time = True):
      if not words: words = words_loaded
      all_num = sum([special_info[p] for p in special_info if p not in remove])
      
      assert "'" in to_find or 'ё' in to_find or '`' in to_find
      if time: utils.timer(supress_print = True)
      
      to_find_data = full_transcript(to_find)
      normal_to_find = normalize(to_find)
      best = [(-float('inf'), '')]
      
      i = 0
      for word in words_loaded:
            # print(word)
            elements = words[word].split('+')
            # elements[0] is current part of speech
            if elements[0] in remove or word == normal_to_find:
                  continue
            
            new, form = get_best_form(elements, to_find_data, words)
            if new > best[0][0] and form != to_find:
                  bisect.insort(best, (new, form, word))
                  if len(best) > n_best:
                        best.pop(0)
            i += 1
            if not i%100:
                  coefficients.print(round(i/all_num*100, 2), '%')
      if time: utils.timer('Sum transcription time:')
      return best


# to_find = wv.morph.normal_forms(normalize(to_find))

def get_source(form):
      for w in words_loaded:
            for form_ in words_loaded[w]:
                  if form_ == form:
                        return w
 

def quick_source(form):
      nform = normalize(form)
      if nform in normal_forms:
            return nform
      
      if len(form) <= 4:
            return get_source(form)
      wstart = nform[:3]
      start = bisect.bisect(sorted_normal_forms, wstart) # select fisrt three letters
      # print(start, wstart)
      for i in sorted_normal_forms[start:]:
            #print(i)
            if normalize(i)[:3] != wstart:
                  break
            if form in words_loaded[i]:
                  return i

      return get_source(form)

def cut_first_n_from_items(sorted_items, n_best):
      return list(map(lambda t: t[1], sorted_items))[:n_best + 1]

def get_best(transcription_sim_words, 
             words_syn = None, n_best = 100,
             weight = 2.0, exclude = []):
      
      if not words_syn:
            return cut_first_n_from_items(transcription_sim_words, n_best)
      
      
      if len(words_syn) > 1:
            field = wv.create_field(*words_syn)
            sim_function = lambda word: - wv.field_distance(field, word) * k_meaning['weight']

      else:
            words_synonym = words_syn[0]
            sim_function = lambda word: - wv.distance(words_synonym, word) * k_meaning['weight']
            
      def key_function(key):
            score, word = key[0], key[2]
            return sim_function(word) + score
      
      sorted_items = sorted(transcription_sim_words, key = key_function, reverse = True)
      
      return cut_first_n_from_items(sorted_items, n_best)

