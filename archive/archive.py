import torch
import torch.nn as nn
import numpy as np
import gensim
import pickle
import csv
import nltk
from pprint import pprint
import random

def dump():
    """
    from dump.py(削除済み)
    ---
    https://code.google.com/archive/p/word2vec/ から得た
    ./GoogleNews-vectors-negative300.binをpickleで直列化するのに使用した
    """
    model_dir = 'embedding/GoogleNews-vectors-negative300.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(model_dir, binary=True)

    with open('embedding/embedding.pickle', 'wb') as f:
        pickle.dump(model, f)



def check_embedding_norm():
    """
    from scratch.py
    ---
    意味の強さとベクトルのノルムは関係するのか調べる(研究とは無関係)
    """
    with open('embedding/embedding.pickle', 'rb') as em:
        model = pickle.load(em)
        with open('nouns/nouns_norm.csv', 'w', newline="") as f_w:
            writer = csv.writer(f_w)
            with open('data/pos_of_words_in_NGSL.csv') as f_r:
                reader = csv.reader(f_r)
                header = ['lemma', 'norm']
                writer.writerow(header)
                for row in reader:
                    lemma = row[0]
                    try:
                        emb = model[lemma]
                        norm = np.linalg.norm(emb)
                        writer.writerow([lemma, norm])
                    except KeyError:
                        writer.writerow([lemma, 'KeyError'])