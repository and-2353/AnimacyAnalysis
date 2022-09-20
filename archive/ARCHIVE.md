## ファイルの概要
### dump.py
https://code.google.com/archive/p/word2vec/ からもってきた`./GoogleNews-vectors-negative300.bin.gz`を7zipで解凍して得た `./GoogleNews-vectors-negative300.bin`をpickleで直列化する
> - `embedding/GoogleNews-vectors-negative300.bin.gz`
> - `embedding/GoogleNews-vectors-negative300.bin`
> - `embedding/embedding.pickle`
> はサイズが大きいので追跡対象外

### extract_nouns.py
`data/NGSL+1.01+by+band.csv` などの外部から入手した単語リストから名詞を抽出する処理など

### preprocessing.py
名詞をembeddingと結合してLDAに使うデータを整備する処理など

### lda.py
LDAなど

### data/
外部から入手した生のデータ・整備途中のデータ・研究に直接的に関係しないデータ など

### nouns/
名詞リスト
つかってないものもあるので整理したい
中身はMEMO「データの整理」にまとめてある

## データの整理
```
data/pos_of_words_in_NGSL # NGSLの全ての語、nltkで品詞推定 2801語
data/nouns_not_filtered.csv # NGSLから語形変化が1つだけ載ってるものを名詞とみなし、抽出、827語
nouns/nouns_v0.csv # 上のコピー、827語
nouns/nouns_v1.csv # v0から手動で名詞でない語を取り除く、作業は[working] まで
nouns/nouns_v2.csv # v0から手動で名詞でない語を取り除く、語数も大幅にカット、作業は[working] まで、81語、
nouns/nouns_v3.csv # filter_nouns_hard()で作成 v0からNLTKで「名詞 in 品詞名」であるものを抽出、716語
nouns/nouns_v4.csv # filter_nouns_soft()で作成 v0からNLTKで「形容詞 not in 品詞名」であるものを抽出、741語
nouns/nouns_v5.csv # v4をコピー 手動で品詞が微妙なものや意味の明確性が低い物を除外しながらラベル付け、作業は[working]まで、701語
nouns/nouns_v6.csv # v4をコピー 100語まで削減、意味の明確性が高いものを選んでラベル付け 100語
nouns/nouns_v7.csv # v6にembeddingを結合したもの 100語
nouns/nouns_v8.csv # V3をコピーして0,1,2,3のラベルをつけたもの 716語
nouns/nouns_v8/nouns_v8.1.csv # v8をコピーしてラベル：3→削除、2→0 にしたもの
nouns/nouns_v8/nouns_v8.1+em.csv # v8.1をコピーしてembeddingと結合したもの
nouns/nouns_v8/nouns_v8.2.csv # v8をコピーしてラベル：3→削除、2→1 にしたもの
nouns/nouns_v8/nouns_v8.2+em.csv # v8.2をコピーしてembeddingと結合したもの
nouns/nouns_v9.csv # BNCから品詞がnとなっているものを抽出、3262語
nouns/nouns_v10.csv # v9をコピーしてラベル付け、3262語
nouns/nouns_random_label/nouns_random_label_1.csv # ランダムラベル① 各ラベルの数はnouns_v8.1 と同一
nouns/nouns_random_label/nouns_random_label_1+em.csv # 上とembeddingの結合
nouns/nouns_random_label/nouns_random_label_2.csv # ランダムラベル① 
nouns/nouns_random_label/nouns_random_label_2+em.csv # 上とembeddingの結合
nouns/nouns_random_label/nouns_random_label_3.csv # ランダムラベル① 
nouns/nouns_random_label/nouns_random_label_3+em.csv # 上とembeddingの結合
nouns/nouns_random_label/nouns_random_label(half).csv # ランダムラベル① 各ラベルの数は半々(0:356,1:355)
nouns/nouns_random_label/nouns_random_label(half)+em.csv # 上とembeddingの結合
```
