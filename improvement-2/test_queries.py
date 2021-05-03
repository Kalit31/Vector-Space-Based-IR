from gensim import corpora,models,similarities
from collections import defaultdict
from gensim.utils import SaveLoad
from nltk.corpus import stopwords
import re
import numpy as np
from bs4 import BeautifulSoup
import nltk
import pickle

with open('corpus_lsi','rb') as corpus_lsi_file:
    corpus_lsi=pickle.load(corpus_lsi_file)

with open('dictionary','rb') as dictionary_file:
    dictionary=pickle.load(dictionary_file)
    
with open('lsi_model','rb') as lsi_model_file:
    lsi_model=pickle.load(lsi_model_file)

corpus_title=np.load('titles_improv2.npy')
index = similarities.MatrixSimilarity(corpus_lsi)

def get_query(query):
  query = query.lower()
  query = re.sub(r'[^\w\s]', '', query)
  query_bow = dictionary.doc2bow(query.lower().split())

  query_lsi = lsi_model[query_bow]
  similarity = index[query_lsi]
  similarity = sorted(enumerate(similarity),key=lambda item: -item[1])

  answertitle=[]
  score=[]
  for i in range(len(similarity)):
      answertitle.append(corpus_title[similarity[i][0]])
      score.append(similarity[i])
      
  for j in range(10):
      print(answertitle[j],"\t",score[j],"\n")

if __name__ == "__main__":
    while(1):
        instructions = 'Press 1 to enter your own query \nPress 2 to get result for a pre-defined query \nPress any other button to exit\nEnter your input '

        x = input(instructions)
        if x == '1':
            query = input("Enter the query you want to search: ")
            get_query(query)
        elif x == '2':
            query = "Space exploration"
            get_query(query)
        else:
            quit(0)