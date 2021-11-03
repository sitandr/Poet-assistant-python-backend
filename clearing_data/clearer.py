import pickle as pkl
import numpy as np


word2index = pkl.load(open('s_word2index.pkl', 'rb'))
index2word = pkl.load(open('s_index2word.pkl', 'rb'))
vectors =    np.load('s_vectors.npy')
vocab =    pkl.load(open('s_vocab.pkl', 'rb'))

normal_forms = pkl.load(open('s_normal_stresses.pkl', 'rb'))

reduced = set(normal_forms.keys())&set(index2word)


print(len(reduced))

reduced = set(filter(lambda t: vocab[t].count > 50, reduced))

print(len(reduced))

normal_forms = {i: normal_forms[i] for i in reduced}

pkl.dump(normal_forms, open('r_normal_stresses.pkl', 'wb'))


vectors = vectors[[index2word[i] in reduced for i in range(len(vectors))]]
np.save('r_vectors.npy', vectors)

index2word = list(filter(lambda t: t in reduced, index2word))
pkl.dump(index2word, open('r_index2word.pkl', 'wb'))

word2index = {index2word[i]: i for i in range(len(index2word))}

pkl.dump(word2index, open('r_word2index.pkl', 'wb'))


