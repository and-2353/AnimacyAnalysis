import torch
import torch.nn as nn
import numpy as np
import gensim
import pickle
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import cross_validate



def load_embedding():
    with open('embedding/embedding.pickle', 'rb') as f:
        model = pickle.load(f)
        return model

def print_df():
    df = pd.read_csv('nouns/nouns_v8/nouns_v8.2+em.csv')
    print(df)

def cross_validate():
    df = pd.read_csv('nouns/nouns_v8/nouns_v8.1+em.csv', encoding='utf-8')

    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    scores = cross_validate(clf, X, y, cv=10, scoring=['accuracy', 'precision', 'recall', 'f1'])

    # 予測, 評価
    print(scores)
    print(scores['test_accuracy'])
    print(scores['test_accuracy'].mean())

def lda():
    df = pd.read_csv('nouns/nouns_v8/nouns_v8.2+em.csv', encoding='utf-8')
    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    clf.fit(X, y)
    print(clf.score(X, y))

    pred = clf.predict(X)
    
    
    for i in range(len(words)):
        if pred[i] == y[i]:
            continue
        else:
            print(f"word:{words[i]}, predict:{pred[i]}, correct:{y[i]}")

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

if __name__ == '__main__':
    #check_prediction()
    lda()
    #print_df()