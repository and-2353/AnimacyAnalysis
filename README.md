# Animacy
###### README最終更新: `2022-06-29`

- **卒業研究** 
- 名詞の有生性についての研究
- 分析対象には英単語を使用している

---

## ファイルの概要
### dump.py
https://code.google.com/archive/p/word2vec/ からもってきた`./GoogleNews-vectors-negative300.bin.gz`を7zipで解凍して得た `./GoogleNews-vectors-negative300.bin`をpickleで直列化する
> - `embedding/GoogleNews-vectors-negative300.bin.gz`
> - `embedding/GoogleNews-vectors-negative300.bin`
> - `embedding/embedding.pickle`
> はサイズが大きいので追跡対象外


## `extracted_nouns` ディレクトリ内のデータの命名規則

|記号|意味|
|:--:|:--|
|`nouns_bnc`|BNCから作成したデータ|
|`nouns_ngsl`|NGSLから作成したデータ|
|`+lbl`|ラベル付け(手動) (0,1,2,3)の4値でラベル付け済|
|`+key`|`embedding/embedding.pickle` の見出し語として存在しないもの(KeyErrorになるもの)を削除済|
|`+bi1`|(0,1,2,3)の4値を(3→削除), (2→0)として2値のラベルに変更済|
|`+bi2`|(0,1,2,3)の4値を(3→削除), (2→1)として2値のラベルに変更済|
|`+em`|見出し語にembedding結合済|
|`rl(1=n)`|ランダムラベル, nはラベル1の数|
|`(n)`|ランダムラベルで同じ1の数のファイルを複数作ったので、その識別番号|

- BNC から作成したデータ：
  - BNC (6318語)のうち品詞が「n」(名詞) である3262語 から作成したデータ群
- NGSL から作成したデータ：
  1. NGSLから語形変化が1つだけ載ってるものを名詞とみなし抽出
  2. そこからNLTKで「名詞 in 品詞名」であるものを抽出
これにより名詞の数は2801語(NGSLすべて)→827語(①)→716語 から作成したデータ群