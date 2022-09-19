import csv
import nltk
import gensim
import pickle
from pprint import pprint

def arrange_data_to_discriminant_analysis():
    """
    ファイルにembeddingを結合する。
        csv(lemma,animacy 形式)を入力とし、
        csv(lemma,d0~d299,animacy)形式を出力する。
    """
    for item in ["_1", "_2", "(half)"]:
        keyerror_num = 0
        with open('embedding/embedding.pickle', 'rb') as em:
            model = pickle.load(em)
            with open(f'nouns/nouns_random_label/3208/nouns_random_label{item}+em.csv', 'w', newline="") as f_w:
                writer = csv.writer(f_w)
                with open(f'nouns/nouns_random_label/3208/nouns_random_label{item}.csv') as f_r:
                    reader = csv.reader(f_r)
                    #_ = next(reader) # skip headline
                    header = create_headline()
                    writer.writerow(header)
                    for row in reader:
                        try:
                            lemma = row[0]
                            animacy = row[1]
                            row_ = [lemma]
                            row_.extend(model[lemma])
                            row_.append(animacy)
                            writer.writerow(row_)
                        except KeyError:
                            print(f"{row[0]}: KeyError")
                            keyerror_num += 1
                            continue
        print(keyerror_num)


def create_headline():
    header = ['lemma']
    for i in range(300):
        header.append('d'+str(i))
    header.append('animacy')
    return header

if __name__ == '__main__':
    arrange_data_to_discriminant_analysis()