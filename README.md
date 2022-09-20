# Animacy
###### README最終更新: `2022-09-20`

- **卒業研究** 
- 名詞の有生性についての研究
- 分析対象には英単語を使用している

---

## ファイル・ディレクトリの概要
- `/archive/` つかってないファイルなど
  - `/data/`つかってないデータ(使ってるファイルも昔の名前で入ってたりする)
  - `archive.py` つかってないコード
  - `ARCHIVE.md` 前使ってたデータとその概要の紐づけ
- `/data/` 加工前のデータ or 加工途中のデータ
  - `/BNC/`
  - `/NGSL/`
  - `embedding` ← gitの追跡対象外 
- `/extracted_data/` 加工途中のデータ or 加工済みデータ
  - `/BNC/`
  - `/NGSL/`
- `/memo/` 進捗報告に使った図、研究メモ
- `dataprocessing.py` データ加工
- `lda.py` LDA,LDA(loo) など

---

## `Git Clone` 後の 環境作成
- `data/embedding/GoogleNews-vectors-negative300.bin.gz`
- `data/embedding/GoogleNews-vectors-negative300.bin`
- `data/embedding/embedding.pickle`

はサイズが大きいので追跡対象外としている。プログラムを動かすには`data/embedding/embedding.pickle` が必要なものが多くあるので、これを用意する。用意の仕方は以下

1. `https://code.google.com/archive/p/word2vec/` から`./GoogleNews-vectors-negative300.bin.gz`をダウンロード・(7zipなどで)解凍
2. 得た `./GoogleNews-vectors-negative300.bin`をpickleで直列化する(直列化は`archive/archive.py` の `dump` 関数 のパスをいじったらできるはず)

---

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