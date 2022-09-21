from sympy import false
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


def loo(file_for_lda, print_missclassified_word=False, cross_tabulation=True):
    df = pd.read_csv(file_for_lda, encoding='utf-8')

    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    loo = LeaveOneOut()
    scores = sklearn.model_selection.cross_validate(clf, X, y, cv=loo)

    error_word_ids = np.where( scores['test_score'] == 0 )
    print('判別的中率：', scores['test_score'].mean())
    print('誤判別語数：', error_word_ids[0].shape)

    # 誤判別語表示
    if print_missclassified_word:
        print('\n|判別を誤った語|予測値|正解ラベル|\n|:--:|:--:|:--:|')
        for word_id in error_word_ids[0]:
            lemma = re.sub('.*\s', '', words[word_id])
            acc_label = y[word_id]
            print(f'|{lemma}||{acc_label}|')
    if cross_tabulation:
        assert len(scores['test_score']) == len(words)
        nums = {}
        for is_right, answer in zip(scores['test_score'], y):
            pa = (int(is_right), answer)
            if pa not in nums:
                nums[pa] = 1
            else:
                nums[pa] += 1
        print(f'クロス集計結果\n,有生,無生\n正解,{nums[(1,1)]},{nums[(1,0)]}\n不正解,{nums[(0,1)]},{nums[(0,0)]}') 
        

def lda(file_for_lda, print_missclassified_word=False):
    df = pd.read_csv(file_for_lda, encoding='utf-8')
    X = df.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y = df['animacy'] # 目的変数: 有生性
    words = df['lemma']

    clf = LDA()
    clf.fit(X, y)
    score = clf.score(X, y)

    pred = clf.predict(X)
    mistake = 0
    for i in range(len(words)):
        if pred[i] == y[i]:
            continue
        else:
            mistake += 1
            if print_missclassified_word:
                print(f"word:{words[i]}, predict:{pred[i]}, correct:{y[i]}")
    print('判別的中率：', score)
    print('誤判別語数：', mistake)



if __name__ == '__main__':
    file_for_lda = 'extracted_nouns/BNC/nouns_bnc+lbl+key+bld+em.csv'
    #lda()
    loo(file_for_lda, False, False)