from translator import check, full_transcript, transcripted_check

import pickle
import utils

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

words = {form for w in words_ for form in words_[w] if (form not in ['-', '']) }
print('united')
import wv
import bisect

# mind the stress!
to_find = "потрея'ю"
assert "'" in to_find

to_find_data = full_transcript(to_find)

field = wv.create_field('исскуство', 'время', 'дорога')

best = [(-float('inf'), '')]

N_BEST_COUNT = 500
N_BEST_MIND = 100
utils.timer()
i = 0
for form in words:
      new = transcripted_check(to_find_data, full_transcript(form))
      if new > best[0][0] and form != to_find:
            bisect.insort(best, (new, form))
            if len(best) > N_BEST_COUNT:
                  best.pop(0)
      i += 1
      if not i%5000:
            print(round(i/len(words)*100, 2), '%')
utils.timer()     
to_find = wv.morph.normal_forms(normalize(to_find))

def get_source(form):
      for w in words_:
            for form_ in words_[w]:
                  if form_ == form:
                        return w

def key_function(key):
      word = wv.morph.normal_forms(normalize(key[1]))[0]
      score = key[0]

      if word not in wv.index2word:
            return 0
      
      # sim = wv.wv.similarity(wv.morph.normal_forms(to_find)[0],
      #                        normalize(wv.morph.normal_forms(word)[0]))
      sim = 1/wv.field_distance(field, word) 
      return sim*score

print('sorting')
print(list(map(lambda t: t[1],
               sorted(best, key = key_function, reverse = True)[:N_BEST_MIND])))
