# Animacy
###### README最終更新: `2022-12-04`

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
- `/extracted_nouns/` 加工途中のデータ or 加工済みデータ
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
2. 得た `./GoogleNews-vectors-negative300.bin`をpickleで直列化する(※直列化には、`archive/archive.py` の `dump` 関数 が利用できる。この関数の場所を変えたり、関数内で参照しているパスをいじったらできるはず)

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
|`+rl(1=n)`|ランダムラベル, nはラベル1の数|
|`(n)`|ランダムラベルで同じラベル数のファイルを複数作ったので、その識別番号|
|`+ani`|有生性ラベルが(1)に該当する語を抽出済|
|`-ani`|有生性ラベルが(0)に該当する語を抽出済|
|`+ani_mid`|有生性ラベルが(1, 2)のいずれかに該当する語を抽出済|
|`+bld`|balanced、有生性ラベル1と0の数を等しくしてある|
|`+collective`|集合的な有生物|
|`+micro`|細胞・微生物・ウイルス|
|`+plant`|植物|
|`+spirit`|神・精霊・霊魂・天使・空想のもの|
|`+special`|気になったもの|
|`+bi3`|(0,1,2,3)の4値を(3→削除), (2→削除)として2値のラベルに変更済|



- BNC から作成したデータ：
  - BNC (6318語)のうち品詞が「n」(名詞) である3262語 から作成したデータ群
- NGSL から作成したデータ：
  1. NGSLから語形変化が1つだけ載ってるものを名詞とみなし抽出
  2. そこからNLTKで「名詞 in 品詞名」であるものを抽出
これにより名詞の数は2801語(NGSLすべて)→827語(①)→716語 から作成したデータ群

## 研究再現について
### 研究1
``` 
[使用したデータ｜データA・データB]
extracted_nouns\BNC\nouns_bnc+lbl+key+bi1+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+bi2+em.csv

[使用したデータ｜ランダムラベル（基準結果）]
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=369)+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=369)(2)+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=369)(3)+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=631)+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=631)(2)+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+rl(1=631)(3)+em.csv

[分析に使用した関数]
lda.py
  loo()
```

### 研究2
``` 
[使用したデータ｜学習]
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(1).csv
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(2).csv
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(3).csv

[使用したデータ｜判別・推論(spirit・collective・micro・plants)]
extracted_nouns\BNC\nouns_bnc+lbl+key+ani_mid+spirit+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+ani_mid+collective+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+ani_mid+micro+em.csv
extracted_nouns\BNC\nouns_bnc+lbl+key+ani_mid+plants+em.csv

[使用したデータ｜animate基準・inanimate基準]
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(1).csv
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(2).csv
extracted_nouns\BNC\nouns_bnc+lbl+key+bld(3).csv

[分析に使用した関数]
・animate基準・inanimate基準の算出
  lda.py
    loo_pred()

・学習～推論
  lda.py
    prediction()
```
