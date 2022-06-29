# 卒業研究
## 目次
[TOC]

## やること(2022/04/28~)
- ~~word embedding さがる→もってくる~~
    - 作る意味はあんまりないよな多分...
- 名詞 抽出・名詞の中で代表的なもの 抽出(ラベル付けしないといけないので、200~400くらい？)
  - 品詞の情報や~~頻度の情報~~は`GoogleNews-vectors`にはなさそうなので、どこかから持ってくる！
  > `model.vocab`に`count`という形で単語の出現回数らしきものが記載されているので頻度の情報はある。どちらにしても品詞の情報は持ってこないといけないと思う。頻度フィルタをどちらでかけるかは実装が簡単なほうにする。
  > Excel で操作できるしNGSLを使おうかな～ 品詞情報はないけど、動詞の屈折など語形変化の情報が載っていて、形容詞は語形変化なし(比較級とかは載ってない)、前置詞も変化なし、名詞は複数形のみ載ってる、動詞は過去・過去分詞・三単現のsなどたくさん載っている みたいな感じで1つだけ語形変化が載ってるものが大体の確率で名詞とみなせそうな気がする。
- 植物など有生性が微妙なものはとりのぞいて、
```
見出し語-embedding-有生ラベル
```
という形に整備

- 判別分析・SVM にかける
- NN にかける←この意味があんまりあるかも微妙だな 表現力の低いモデルで判別できてないなら意味はない？でも本当に有生性が予測できないならNNでもできないしできるかどうかは意味があるといえるか...
- 次元削減してからかける←結果は変わるのかな～

> 本当は全く判別しようのないラベルづけや逆に明らかに判別できそうな（名詞・形容詞とか）も判別できるかをコントロール？として同じ判別分析やらSVM/NNやらにかけたほうがいい


その後、
- 有生性を明示的に結合して、精度は上がるかみたいなこと(ELMo寄り)
  - embeddingに有生性の情報が含まれていない/明らかに含まれているとは言えない みたいな状況なら、「ではこの情報は常識理解を助けるからあったほうがいいと思う」と仮説が立って、この方向に持っていけてる。さらに精度の向上が果たせることが理想ではある（そうすれば、意味理解に有生性の概念は助けになることが示唆できる）今は全然無理なことだけど、有生性によって文法的に違いが出る言語ではその影響は強いかみたいなことも知りたい。
  
## やったこと
### モデルの入手
https://code.google.com/archive/p/word2vec/ からもってきた`./GoogleNews-vectors-negative300.bin.gz`を7zipで解凍し、`./GoogleNews-vectors-negative300.bin`を得る

多分(シンプルな)word2vec。fasttext とかじゃないと思うけどこれ何のモデルのembedding なのかちゃんと調べないとな

### 格納
https://kento1109.hatenablog.com/entry/2018/03/15/153652 を参考に、gensimをつかって読み込み・pickleで直列化

### モデルの調査
詳細は[モデルの詳細](#モデルの詳細)

### 判別分析・SVMにかけるデータの整備
1. NGSLをつかって名詞を抽出
> 語形変化が1つだけ載ってるものを名詞とみなし、抽出
2. 手動で名詞でない(名詞ではないもの, または名詞以外のほかの品詞のほうが一般的(主観)なもの)を取り除く

```
data/nouns_not_filtered.csv # 1によって得たもの
nouns/nouns_v0.csv # 上のコピー
nouns/nouns_v1.csv # 2によって得たもの
```

3. 判断基準が難しく明確なルールで分けたいと思い、NGSL上にある単語のうち、単語をNLTKによる品詞推定の入力とし、以下の形式でcsv出力。
> ゆくゆくNNに入れて精度向上を見据えているので、NNが学習するコーパスにある語のうち有生性のある名詞だけに質的変数1を追加/それ以外には0を追加 みたいなことをしたい。
> コーパス全体のラベル付けは人力では難しいので)、自動化したかった
> ただし、このラベル付けはNNの入力とするコーパスのラベル付けにもそのまま適用できるわけではない。以下のような問題がある
> - そもそも名詞のラベル付けが自動化できても、有生性のラベル付けを自動化する方法がないという問題もある
> - 文は形態素解析結果どの語が名詞句か判別することはできるので、コーパス中の名詞にラベルを付けるのは辞書や単語リストから名詞を抽出するのとは異なる問題である 

[NLTKの使い方をいろいろ調べてみた](https://qiita.com/m__k/items/ffd3b7774f2fde1083fa)


`単語, 品詞タグ, 品詞名(日本語)` 
出力先：`data/pos_of_words_in_NGSL.csv` 
→ 動詞と名詞の二つの品詞を持つ語が名詞になりやすいよう。以下など
```
help,NN,名詞
ask,NN,名詞
meet,NN,名詞
```
beとかはさすがに動詞として解析されたが、ここまで動詞が一般的な語が名詞になってしまうと、名詞を取り出しているという感じではない。→NLTKは微妙かな...。
→local やfinancial のような形容詞性の高い語がngslから誤抽出されている & それらは大体nltk では形容詞として分類されている ので、行程2→形容詞を排除 にすれば結構良い感じでフィルターできるかも。動詞性の高い語はnltkでは名詞になりやすく排除できないという問題点はあるがその数は少なそう

>  辞書中の単語は
>   - 名詞の用例が再頻出の語(100回中50~60回程度は名詞で使われる)
>   - 名詞の用例が用例のほとんどを占める語(100回中80~90回以上は名詞で使われる)
>   - 名詞の用例が用例の全てを占める語(100回中100回名詞で使われる)
> のどれを名詞性の高い語として抽出するかという問題もある。
  
4. 名詞性の高い語を単語リストから抽出するのはけっこう難しい問題であることが分かったので、正確なラベル付けやデータ量の確保はいったん後回しにする。とりあえず、名詞フィルターの正確性はいったん後回しにして、20個20個ずつ名詞らしさが高い名詞を自分で選んで判別分析にかけることにする！
名詞の選び取り結果は、出力先：`nouns/nouns_v6.csv` 

### データの整備(再)
ラベル付けを行う。
有生性が微妙なものは削除するのではなく、その単語をメモしておきたいので、「不明ラベル」をつけておいてあとでプログラムを使って別の場所に転記できるようにする。
#### ラベルのルール
```
0: 有生性なし
1: 有生性あり
2: 有生性があるかないか迷ったもの←あとでカテゴリわける(その時主成分分析してもいいかも)
3: 削除するもの(形容詞性による削除のルールは未定)
```
- 人の役職的なものは~~2にする~~1にする family は2

|ラベル|意味|例|語数|
|:--:|:--:|:--:|:--:|
|0|有生性なし||570|
|1|有生性あり||109|
|2|有生性があるかないか迷ったもの|agent<br>family<br>god|32|
|3 |削除するもの|nobody<br>形容詞性の高い語<br>代名詞|5|




## モデルの詳細
`model = gensim.models.KeyedVectors.load_word2vec_format(model_dir, binary=True)`

は `<class 'gensim.models.keyedvectors.Word2VecKeyedVectors'>` 型のインスタンス
メンバ変数とその値の型は以下の通り
|メンバ変数|値の型|備考|
|:--:|:--:|:--:|
|vectors |<class 'numpy.ndarray'>|300万×300|
|vocab |<class 'dict'> ||
|vector_size |<class 'int'>|300|
|index2word |<class 'list'>||
|vectors_norm| <class 'NoneType'>||

> ※`model['dog']` or `model.wv['dog']` とかで分散表現にアクセスできるので、`index2word`とか`vectors`とか`vocab`とか使う必要ないかも

### 変数

#### vectors
- <class 'numpy.ndarray'>
  - 2次元
  - shape = (3000000, 300)

#### vocab
- dict
  - key: str (見出し語)
  - value: <gensim.models.keyedvectors.Vocab object>
    - count (多分登場した数)
    - index
```
vars(model.vocab['dog'])
>>> {'count': 2997957, 'index': 2043}
```
ここに 分散表現はない！

#### vector_size
- int
- 定数(300)
> 分散表現の次元数が300

#### index2word
- list

```
pprint(model.index2word)
--> 見出し語が次々に出力された
ABC順にソートされてる感じでは特にない
```
添字がindexってことかな～ それならタプルのほうがいいんじゃないの？とは少し思う

`len(model.index2word)` は 3,000,000だったので、語彙数が300万だと思う！

#### vectors_norm
NoneType、値はNone、インスタンス生成時に値が登録されてない変数
ベクトルのノルムはベクトルの長さ、多分使わないかな～と思う

## 疑問点など
### wv とは
内部のembedding は`model.wv` によって得ているの何なんだろう wvもメンバ変数てこと？ちょっとよくわかってない
> wvはスーパークラスの変数で__dict__では表示されない みたいなことはあり得る？
```
print(model['dog'] == model.wv['dog'])
>>> 要素ごと表示, だけど全部True

print(model == model.wv)
>>> True

print(model is model.wv)
>>> True <--- IDも同じ！
```
`model`, `model.wv` の`type`は同じ(`Word2VecKeyedVectors`)
`model.__dict__.items()` と `model.wv.__dict__.items()` も同じ
`wv` を使う意味はあんまり分からないかなと思う。
> `print(model.wv.wv.wv.wv.wv)` とか書いても動く なんだこれ

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
```

## 補足
- gensim内にあるモデルの読み込みもできるっぽい
```
import gensim.downloader as api
model = api.load('glove-wiki-gigaword-50')
```
(あまり詳しく書いてないけど)参考：https://kento1109.hatenablog.com/entry/2018/03/15/153652

## 参考/使えそうなページ
- https://code.google.com/archive/p/word2vec/
- https://www.kaggle.com/code/abdelhek115/googlenews-vectors-negative300
- https://kento1109.hatenablog.com/entry/2018/03/15/153652
- https://ishitonton.hatenablog.com/entry/2019/06/20/181758
- https://qiita.com/m__k/items/ffd3b7774f2fde1083fa