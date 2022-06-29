import csv
import nltk
import gensim
import pickle
from pprint import pprint
import numpy as np

def check_embedding_norm():
    """
    意味の強さとベクトルのノルムは関係するのか調べる
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

if __name__ == '__main__':
    check_embedding_norm()