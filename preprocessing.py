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
    with open('embedding/embedding.pickle', 'rb') as em:
        model = pickle.load(em)
        with open('nouns/nouns_random_label/nouns_random_label(half)+em.csv', 'w', newline="") as f_w:
            writer = csv.writer(f_w)
            with open('nouns/nouns_random_label/nouns_random_label(half).csv') as f_r:
                reader = csv.reader(f_r)
                _ = next(reader) # skip headline
                header = create_headline()
                writer.writerow(header)
                for row in reader:
                    lemma = row[0]
                    animacy = row[1]
                    row_ = [lemma]
                    row_.extend(model[lemma])
                    row_.append(animacy)
                    writer.writerow(row_)


def create_headline():
    header = ['lemma']
    for i in range(300):
        header.append('d'+str(i))
    header.append('animacy')
    return header

if __name__ == '__main__':
    arrange_data_to_discriminant_analysis()