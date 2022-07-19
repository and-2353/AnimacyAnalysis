import torch
import torch.nn as nn
import numpy as np
import gensim
import pickle
from pprint import pprint
import pandas as pd
import sklearn
import re
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import cross_validate
from sklearn.model_selection import LeaveOneOut

def load_embedding():
    with open('embedding/embedding.pickle', 'rb') as f:
        model = pickle.load(f)
        return model

def print_df():
    df = pd.read_csv('nouns/nouns_v8/nouns_v8.2+em.csv')
    print(df)

def cross_validate():
    df = pd.read_csv('nouns/nouns_random_label/nouns_random_label_1+em.csv', encoding='utf-8')

    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    loo = LeaveOneOut()
    #scores = cross_validate(clf, X, y, cv=12, scoring=['accuracy', 'precision', 'recall', 'f1'])
    #scores = cross_validate(estimator=clf, X=X, y=y, cv=loo)
    scores = sklearn.model_selection.cross_validate(clf, X, y, cv=loo)

    # 予測, 評価
    # print(scores)
    # print(scores['test_accuracy'])
    # print(scores['test_accuracy'].mean())
    error_word_ids = np.where( scores['test_score'] == 0 )
    print('判別的中率：', scores['test_score'].mean())
    print('誤判別語数：', error_word_ids[0].shape)
    print('\n|判別を誤った語|予測値|正解ラベル|\n|:--:|:--:|:--:|')
    ##print(scores)
    for word_id in error_word_ids[0]:
        lemma = re.sub('.*\s', '', words[word_id])
        acc_label = y[word_id]
        print(f'|{lemma}||{acc_label}|')
        

def lda():
    df = pd.read_csv('nouns/nouns_random_label/nouns_random_label(half)+em.csv', encoding='utf-8')
    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    clf.fit(X, y)
    print(clf.score(X, y))

    pred = clf.predict(X)
    mistake = 0
    for i in range(len(words)):
        if pred[i] == y[i]:
            continue
        else:
            print(f"word:{words[i]}, predict:{pred[i]}, correct:{y[i]}")
            mistake += 1
    print('number of mistake is ', mistake)

def check_mistake_in_cross_validate():
    """
    cross_validate で判別をミスした単語を列挙する
    完成してない
    """
    
    df = pd.read_csv('nouns/nouns_v7.csv', encoding='utf-8')

    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    scores = cross_validate(clf, X, y, cv=10, scoring=['accuracy', 'precision', 'recall', 'f1'])

    # 予測, 評価
    print(scores)
    print(scores['test_accuracy'])
    print(scores['test_accuracy'].mean())

def temp():
    df = pd.read_csv('nouns/nouns_v8/nouns_v8.2+em.csv', encoding='utf-8')
    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']
    print(X)

if __name__ == '__main__':
    #check_prediction()
    #lda()
    #print_df()
    #temp()
    cross_validate()
    #check_mistake_in_cross_validate()