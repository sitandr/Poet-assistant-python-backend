from assonanses import check

import pickle


def getstressed(word):
      res = words[word][0]
      if res == '-':
            return words[word][1]
      return res

def normalize(word):
      return word.replace('`', '').replace("'", '')

words = pickle.load(open('normal_stresses.pkl', 'rb'))
# word_normal_form_list = [(key, getstressed(key))
#                          for key in words]
words = {form for w in words for form in words[w] if (form not in ['-', '']) }
print('united')
import wv
import bisect

# mind the stress!
to_find = "любо'вь"
field = wv.create_field('битва', 'удар', 'смерть')

best = [(-float('inf'), '')]

N_BEST_COUNT = 300
N_BEST_MIND = 100

i = 0
for form in words:
      new = check(to_find, form)
      if new > best[0][0] and form != to_find:
            bisect.insort(best, (new, form))
            if len(best) > N_BEST_COUNT:
                  best.pop(0)
      i += 1
      if not i%1000:
            print(round(i/len(words)*100, 2), '%')
            
to_find = wv.morph.normal_forms(normalize(to_find))

def key_function(key):
      word = wv.morph.normal_forms(normalize(key[1]))[0]
      score = key[0]

      if word not in wv.wv:
            return 0
      
      # sim = wv.wv.similarity(wv.morph.normal_forms(to_find)[0],
      #                        normalize(wv.morph.normal_forms(word)[0]))
      sim = 1/wv.field_distance(field, word) 
      return sim*score

print('sorting…')
print(sorted(best, key = key_function, reverse = True)[:N_BEST_MIND])
