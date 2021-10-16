from gensim.models import KeyedVectors
import numpy as np
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
wv = KeyedVectors.load('just_vectors.kv')
##
##new_vectors = []
##new_vocab = {}
##i = 0
####clear
##for word in wv.vocab:
##      index = wv.vocab[word].index
##      if wv.vocab[word].count < 10:
##            wv.index2word.remove(word)
##      else:
##            new_vectors.append(wv.vectors[index])
##            new_vocab[word] = wv.vocab[word]
##      i += 1
##      if not i%100:
##            print(i, len(wv.vocab))
##            
##wv.vectors = np.array(new_vectors)
##wv.vocab = new_vocab
##print('Clear ended')
wv.index2word = np.array(wv.index2word)
wv.vectors /= (np.sum(wv.vectors**2, -1)**0.5)[:, np.newaxis]



def word2index(word):
      return np.where(wv.index2word == word)

def best_that(function, array = wv.index2word, n = 100):
      func = np.vectorize(function)
      applied = func(array)
      return array[np.argsort(applied)[:n]]

def word_filter(function, array = wv.index2word):
      func = np.vectorize(function)
      return array[np.where(func(array))]

def create_field(*words):
      vects = wv.vectors[np.where(np.isin(wv.index2word, words))]
      mu = np.average(vects, 0)
      sigma = (np.amax(vects, axis = 0) - np.amin(vects, axis = 0))**2 + 0.1
      return (mu, sigma)

def field_distance(field, word):
      return np.sum((word2index(word) - field[0])**4 / field[1])**(1/10)

def best_by_field(field, array = wv.index2word, n = 100):
      if array is not wv.index2word:
            vects = wv.vectors[np.where(np.isin(wv.index2word, array))]
      else:
            vects = wv.vectors
      return array[np.argsort(np.sum((vects - field[0])**4 / field[1], axis = -1))[:n]]

# my = create_field('капюшон', 'смерть', 'пожинать')
# print(best_by_field(my, word_filter(lambda t: len(t) > 3 and t[0] == t[3])))
