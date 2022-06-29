# Animacy
###### README最終更新: `2022-06-29`

卒業研究 
名詞の有生性についての研究
分析対象には英単語を使用している

---

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