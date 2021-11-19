import os, sys
import yaml
from pathlib import Path
import pickle as pkl
import numpy as np


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

file_path = Path(application_path)

TRASCRIPT_CONFIG = yaml.safe_load(open(file_path/'config/convertation.yaml',
                                       encoding = 'utf-8'))
coefficients = yaml.safe_load(open(file_path/'config/coefficients.yaml',
                                       encoding = 'utf-8'))

word2index =          pkl.load(open(file_path/'res/r_word2index.pkl', 'rb'))
index2word = np.array(pkl.load(open(file_path/'res/r_index2word.pkl', 'rb')))
vectors =    np.load               (file_path/'res/r_vectors.npy')

words_loaded = pkl.load(open(file_path/'res/r_min_zaliz.pkl'   , 'rb'))
special_info = pkl.load(open(file_path/'res/r_special_info.pkl', 'rb'))
