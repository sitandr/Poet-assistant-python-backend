from translator import check, full_transcript, transcripted_check

import pickle
import utils

import wv
import bisect

basic_fields = {'Art': ['исскуство', 'свет', 'огонь', 'творчество', 'вдохновение', 'мечта'],
                'Battle': ['битва', 'кровь', 'ярость', 'храбрость', 'герой', 'зло'],
                'Love': ['страсть', 'влечение', 'красота', 'сердце', 'поцелуй'],
                'Epic': ['мощь', 'великий', 'просветление', 'мудрость'],
                'Fear': ['страх', 'опасность', 'побег'],
                'Dark': ['тьма', 'смерть', 'труп', 'отчаяние', 'безумие']}

def getstressed(word):
      res = words[word][0]
      if res == '-':
            return words[word][1]
      return res

def normalize(word):
      return word.replace('`', '').replace("'", '')


words_loaded = pickle.load(open('normal_stresses.pkl', 'rb'))

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
             words_field = None, words_synonym = None,
             weight = 0.5):
      assert words_field or words_synonym

      cash_normal_f = {}

      def get_nf(w):
            if w not in cash_normal_f:
                  cash_normal_f[w] = wv.morph.normal_forms(normalize(w))[0]

            return cash_normal_f[w]
      
      def transform(key):
            return key[0], get_nf(key[1])
      
      if words_field:
            field = wv.create_field(*words_field)
            def key_function(key):
                  score, word = transform(key)
                  if word not in wv.index2word:
                        sim = -100
                  else:
                        sim = - wv.field_distance(field, word) * weight
                  return sim + score

      elif words_synonym:
            words_synonym = wv.morph.normal_forms(normalize(words_synonym))[0]
            
            def key_function(key):
                  score, word = transform(key)
                  if word not in wv.index2word:
                        sim = -100
                  else:
                        sim = - wv.distance(words_synonym, word * weight)
                  return sim + score
      
      sorted_words = list(map(lambda t: t[1], sorted(transcription_sim_words, key = key_function, reverse = True)))
      unic_words = []

      for i in sorted_words:
            if get_nf(i) not in unic_words:
                  unic_words.append(i)
            if len(unic_words) >= n_best

      return unic_words


# filter_remove_parts_of_speech([])
# mind the stress!
# to_find = "иде'и"



# best = get_best_by_transcription(to_find, words = all_forms_set)
# print(best)
# print(get_best(best, words_field = ))
