import csv
import nltk
import gensim
import pickle
from pprint import pprint
import numpy as np
import random

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
        zeros = [0 for i in range(1604)]
        ones = [1 for i in range(1604)]
        labels = zeros + ones
        random.shuffle(labels)

        with open(f'nouns/nouns_random_label/3208/nouns_random_label(half).csv', 'w', newline="") as f: # 出力先
            writer = csv.writer(f)
            # header = ['lemma', 'animacy']
            # writer.writerow(header)
            with open('nouns/nouns_random_label/3208/nouns_random_label_temp.csv') as f_r:
                    reader = csv.reader(f_r)
                    _ = next(reader) # skip headline
                    for label, row in zip(labels, reader):
                        lemma = row[0]
                        writer.writerow([lemma, label])
        break


def remove_lemma_with_no_embedding():
    """
    embedding.pickeの見出し語として登録されていない語を取り除く。
        csv(lemma,animacy) 形式を入力とし、
        csv(lemma,animacy) 形式を出力する。
    """
    keyerror_num = 0
    with open('embedding/embedding.pickle', 'rb') as em:
        model = pickle.load(em)
        with open('nouns/nouns_random_label/3208/nouns_random_label_temp.csv', 'w', newline="") as f_w:
            writer = csv.writer(f_w)
            with open('nouns/nouns_v10/nouns_v10.csv') as f_r:
                reader = csv.reader(f_r)
                
                for row in reader:
                    try:
                        lemma = row[0]
                        animacy = row[1]
                        _ = model[lemma] # model[lemma] がなければ except へ
                        if animacy == "3":
                            continue
                        writer.writerow(row)
                    except KeyError:
                        print(f"{row[0]}: KeyError")
                        keyerror_num += 1
                        continue
    print(keyerror_num)

if __name__ == '__main__':
    #check_embedding_norm()
    random_labeling()
    #remove_lemma_with_no_embedding()