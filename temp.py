import pickle
file_em = 'data/embedding/embedding.pickle'
with open(file_em, 'rb') as em:
    model = pickle.load(em)
    # print(model['green']==model['Green'])
    print(model['virus'])