import csv
import nltk
import gensim
import pickle
from pprint import pprint
import numpy as np
import random

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


def random_labeling():
    """
    6/28 進捗を受け、判別的中率が99%を超えていたので
    判別的中率がどのくらい高いか、ラベルの偏りが悪影響を与えていないかを調べる
    ランダムにラベル付け(各ラベルの数は同じ)して判別分析するためのラベル付け
    有生性に厳格(偏っているほう)で調査
    有生性あり：602
    有生性なし：109
    
    """
    for i in range(1,4):
        zeros = [0 for i in range(355)]
        ones = [1 for i in range(356)]
        labels = zeros + ones
        random.shuffle(labels)

        with open(f'nouns/nouns_random_label/nouns_random_label(half).csv', 'w', newline="") as f: # 出力先
            writer = csv.writer(f)
            header = ['lemma', 'animacy']
            writer.writerow(header)
            with open('nouns/nouns_v8.csv') as f_r:
                    reader = csv.reader(f_r)
                    _ = next(reader) # skip headline
                    for label, row in zip(labels, reader):
                        lemma = row[0]
                        writer.writerow([lemma, label])
        break
                    

if __name__ == '__main__':
    #check_embedding_norm()
    random_labeling()