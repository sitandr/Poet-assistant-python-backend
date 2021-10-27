import numpy as np
import pymorphy2
import pickle as pkl

morph = pymorphy2.MorphAnalyzer()

word2index = pkl.load(open('r_word2index.pkl', 'rb'))
index2word = np.array(pkl.load(open('r_index2word.pkl', 'rb')))
vectors =    np.load('r_vectors.npy')


def word2vector(word):
      return vectors[word2index[word]]

def words2vectors(words):
      return vectors[np.where(np.isin(index2word, words))]

def best_that(function, array = index2word, n = 100):
      func = np.vectorize(function)
      applied = func(array)
      return array[np.argsort(applied)[:n]]

def word_filter(function, array = index2word):
      func = np.vectorize(function)
      return array[np.where(func(array))]

def filter_by_parts_of_speech(words, removed_speech_parts):
      if len(removed_speech_parts) == 0:
            return words
      removed_speech_parts = set(removed_speech_parts)
      words_ = set()
      for word in words:
            if not set(morph.tag(word)[0].grammemes)&removed_speech_parts:
                  words_.add(word)
      return words_

def create_field(*words):
      vects = vectors[np.where(np.isin(index2word, words))]
      mu = np.average(vects, 0)
      sigma = np.std(vects, axis = 0)
      return (mu, sigma)

def field_distance(field, word):
      return np.sum((word2index[word] - field[0])**2 / field[1])**(1/10)

def best_by_field(field, array = index2word, n = 100):
      if array is not index2word:
            vects = words2vectors(array)
      else:
            vects = vectors
      return array[np.argsort(np.sum((vects - field[0])**4 / field[1], axis = -1))[:n]]

def distance(word1, word2):
      "Max 2, min — 0"
      return np.sum((word2vector(word1) - word2vector(word2))**2, axis = -1)

if __name__ == '__main__':
      my = create_field(*['битва', 'кровь', 'ярость', 'храбрость', 'герой', 'зло'])
      for i in ['слово', 'слава', 'компьютер', 'кусать', 'герой', 'сладкий', 'бизнес']:
            print(i, field_distance(my, i))
      print(best_by_field(my))
