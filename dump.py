import torch
import torch.nn as nn
import numpy as np
import gensim
import pickle

model_dir = 'embedding/GoogleNews-vectors-negative300.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_dir, binary=True)

with open('embedding/embedding.pickle', 'wb') as f:
    pickle.dump(model, f)



