from translator import check, full_transcript, transcripted_check

import pickle
import utils

import wv
import bisect

def getstressed(word):
      res = words[word][0]
      if res == '-':
            return words[word][1]
      return res

def normalize(word):
      return word.replace('`', '').replace("'", '')

words_ = pickle.load(open('normal_stresses.pkl', 'rb'))

# word_normal_form_list = [(key, getstressed(key))
#                          for key in words]

all_forms_set = {form for w in words_
                 for form in words_[w]
                 if (form not in ['-', ''])}



def get_best_by_transcription(to_find,
                              words = all_forms_set,
                              n_best = 500,
                              time = True):
      if time: utils.timer(supress_print = True)
      
      to_find_data = full_transcript(to_find)
      best = [(-float('inf'), '')]
      
      i = 0
      for form in words:
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
      for w in words_:
            for form_ in words_[w]:
                  if form_ == form:
                        return w
 


def get_best(transcription_sim_words, n_best = 100,
             words_field = None, words_synonym = None):
      assert words_field or words_synonym

      
      def transform(key):
            word = wv.morph.normal_forms(normalize(key[1]))[0]
            score = key[0]
            return score, word
      
      if words_field:
            field = wv.create_field(*words_field)
            def key_function(key):
                  score, word = transform(key)
                  if word not in wv.index2word:
                        return 0
                  
                  sim = 1/wv.field_distance(field, word) 
                  return sim*score

      elif words_synonym:
            words_synonym = wv.morph.normal_forms(normalize(words_synonym))[0]
            
            def key_function(key):
                  score, word = transform(key)
                  if word not in wv.index2word:
                        return 0
                  
                  sim = wv.distance(words_synonym,
                                    wv.morph.normal_forms(normalize(word))[0])
                  return sim*score
      
      return list(map(lambda t: t[1],
               sorted(transcription_sim_words, key = key_function, reverse = True)[:n_best]))

# mind the stress!
to_find = "ря'ю"
assert "'" in to_find

print(get_best(get_best_by_transcription(to_find), words_synonym = 'май'))
