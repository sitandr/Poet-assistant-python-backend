import numpy as np
from resource_importer import word2index, index2word, vectors




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

def create_field(*words):
      vects = vectors[np.where(np.isin(index2word, words))]
      mu = np.average(vects, 0)
      sigma = np.std(vects, axis = 0)
      return (mu, sigma)

def field_distance(field, word):
      return np.sum(np.absolute((word2vector(word) - field[0]))**0.5)**4/900_000

def best_by_field(field, array = index2word, n = 100):
      if array is not index2word:
            vects = words2vectors(array)
      else:
            vects = vectors
      return array[np.argsort(np.sum(np.absolute((vects - field[0]))**0.5 / field[1], axis = -1))[:n]]

def distance(word1, word2):
      "Max 2, min — 0"
      return np.sum((word2vector(word1) - word2vector(word2))**2, axis = -1)

if __name__ == '__main__':
      my = create_field(*['битва', 'кровь', 'ярость', 'храбрость', 'герой', 'зло'])
      for i in ['слово', 'слава', 'компьютер', 'кусать', 'герой', 'сладкий', 'бизнес']:
            print(i, field_distance(my, i))
            print(i, distance('битва', i))
      print(best_by_field(my))
