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
        #print(f'クロス集計結果\n,有生,無生\n正解,{nums[(1,1)]},{nums[(1,0)]}\n不正解,{nums[(0,1)]},{nums[(0,0)]}')
        TP, TN, FP, FN = nums[(1,1)], nums[(1,0)], nums[(0,0)], nums[(0,1)]
        precision = TP/(TP+FP)
        recall = TP/(TP+FN)
        f_measure = (2*precision*recall)/(precision+recall)
        print(f"適合率(precision): {precision}, 再現率(recall): {recall}, F値(f-measure): {f_measure}")
        

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


def prediction(file_for_fit, file_for_pred):
    
    # 0/1 のデータにfit
    df_fit = pd.read_csv(file_for_fit, encoding='utf-8')
    X_fit = df_fit.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    y_fit = df_fit['animacy'] # 目的変数: 有生性
    words = df_fit['lemma']
    clf = LDA()
    clf.fit(X_fit, y_fit)

    # 特定のデータでpredict
    df_pred = pd.read_csv(file_for_pred, encoding='utf-8')
    X_pred = df_pred.drop(['lemma', 'animacy'], axis=1) # 説明変数: embedding
    words_pred = df_pred['lemma']
    pred = clf.predict(X_pred)
    pred_proba = clf.predict_proba(X_pred)
    print('\n|語|予測|有生性なし(0)に所属する確率|\n|:--:|:--:|:--:|')
    for i, word in enumerate(words_pred):
        print(f'|{word}|{pred[i]}|{pred_proba[i][0]:.4%}|')


if __name__ == '__main__':
    file_for_fit = 'extracted_nouns/BNC/nouns_bnc+lbl+key+bld+em.csv'
    file_for_pred = 'extracted_nouns/BNC/nouns_bnc+lbl+key+ani_mid+plant+em.csv'
    # lda()
    # loo(file_for_lda, False, True)
    prediction(file_for_fit, file_for_pred)