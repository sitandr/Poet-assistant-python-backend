
from translator import check, full_transcript, transcripted_check

import pickle
import utils

import wv
import bisect

from coefficients import k_meaning

def getstressed(word):
      res = words[word][0]
      if res == '-':
            return words[word][1]
      return res

def normalize(word):
      return word.replace('`', '').replace("'", '')

words_loaded = pickle.load(open('r_normal_stresses.pkl', 'rb'))
normal_forms = set(words_loaded.keys())
sorted_normal_forms = sorted(normal_forms)

# word_normal_form_list = [(key, getstressed(key))
#                          for key in words]

def filter_remove_parts_of_speech(remove = ['VERB', 'INFN']):
      
      words_filtered = wv.filter_by_parts_of_speech(words_loaded, remove)
      return {form for w in words_filtered
                       for form in words_loaded[w]
                       if (form not in ['-', ''])}

def get_best_by_transcription(to_find,
                              words,
                              n_best = 500,
                              time = True):
      assert "'" in to_find
      if time: utils.timer(supress_print = True)
      
      to_find_data = full_transcript(to_find)
      best = [(-float('inf'), '')]
      
      i = 0
      for form in words:
            # print(form)
            new = transcripted_check(to_find_data, full_transcript(form))
            
            if new > best[0][0] and form != to_find:
                  bisect.insort(best, (new, form))
                  if len(best) > n_best:
                        best.pop(0)
            i += 1
            if not i%5000:
                  print('\r', round(i/len(words)*100, 2), '%', end = ' ')
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
      
      cash_normal_f = {}

      def get_nf(w):
            if w not in cash_normal_f:
                  cash_normal_f[w] = quick_source(w)

            return cash_normal_f[w]

      unic_words = []
      norm_forms = [get_nf(i) for i in exclude]
      
      for i in transcription_sim_words:
            f = get_nf(i[1])
            if f not in norm_forms:
                  unic_words.append(i)
                  norm_forms.append(f)
      
      
      if len(words_syn) > 1:
            field = wv.create_field(*words_syn)
            sim_function = lambda word: - wv.field_distance(field, word) * k_meaning['weight']

      else:
            words_synonym = get_nf(words_syn[0])
            sim_function = lambda word: - wv.distance(words_synonym, word) * k_meaning['weight']
            
      def key_function(key):
            score, word = key[0], get_nf(key[1])
            return sim_function(word) + score
            
      sorted_items = sorted(unic_words, key = key_function, reverse = True)
      
      return cut_first_n_from_items(sorted_items, n_best)


# filter_remove_parts_of_speech([])
# mind the stress!
# to_find = "иде'и"



# best = get_best_by_transcription(to_find, words = all_forms_set)
# print(best)
# print(get_best(best, words_field = ))
