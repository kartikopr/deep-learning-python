import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np 
import re
import nltk

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
%matplotlib qt

data = pd.read_csv('coba.csv', sep='\t')
kata = data.iloc[:, [1]]

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

STOP_WORDS_IDN = stopwords.words('indonesian')

corpus = []
for i in range(0, 575):
    review = re.sub('[^a-zA-Z]', ' ', data['0'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(STOP_WORDS_IDN)]
    review = ' '.join(review)
    corpus.append(review)
corpus_2 = []    
for i in range(0, 575):
    a = corpus[i]
    a = a.split()
    corpus_2.append(a)
    
model = word2vec.Word2Vec(corpus_2, size = 100, window = 20, min_count=1, workers = 4, hs=1, negative=1)

labels = []
tokens = []

for word in model.wv.vocab:
    tokens.append(model[word])
    labels.append(word)

tsne_model = TSNE(perplexity=40, n_components=2, init = 'pca', n_iter=250, random_state=0)
new_values = tsne_model.fit_transform(tokens)

x = []
y = []

for value in new_values:
    x.append(value[0])
    y.append(value[1])
    
plt.figure(figsize=(16, 16))
for i in range(len(x)):
    plt.scatter(x[i], y[i])
    plt.annotate(labels[i], 
                 xy=(x[i], y[i]), xytext=(5, 2),
                 textcoords='offset points',
                 ha = 'right',
                 va='bottom')
plt.show()

score = []

for i in range(len(corpus)):
    score.append(model.score([corpus[i].split()]))


    