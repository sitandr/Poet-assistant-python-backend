import pickle as pkl
import numpy as np


word2index = pkl.load(open('s_word2index.pkl', 'rb'))
index2word = pkl.load(open('s_index2word.pkl', 'rb'))
vectors =    np.load('s_vectors.npy')
vocab =    pkl.load(open('s_vocab.pkl', 'rb'))

normal_forms = pkl.load(open('s_normal_stresses.pkl', 'rb'))

reduced = set(index2word) - set(normal_forms.keys())
to_find = [i for i in index2word if i in reduced]
