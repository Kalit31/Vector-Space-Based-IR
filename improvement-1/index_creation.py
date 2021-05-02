# -*- coding: utf-8 -*-
"""index_creation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15HgZsH3IGz-i0HwmC19yd3H_W6JSu_va
"""

#from google.colab import drive
#drive.mount('/content/drive',force_remount=True)

#pip install beautifulsoup4

import bs4 as bs 
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import string
import pickle
import sys
nltk.download('punkt')
import warnings
warnings.filterwarnings("ignore")

#from google.colab import drive
#drive.mount('/content/drive')

'''
Intialize data structures

vocabulary maps a token id to token object
  vocabulary{
    0 : term0 
    1 : term1
  }

reverse_vocabulary maps a token value to token object
  reverse_vocabulary{
    term0.word :term0
    term1.word :term1
  }

all_docs: stores all the documents found in the file

inverted_index: stores the inverted index for the corpus

'''
vocabulary = {}
reverse_vocabulary ={}
all_docs = {}
inverted_index = {}

def clean_text(file_text):
  '''
    Takes a text as input and returns a list of splitted tokens, excluding punctuations

    eg: s='Good muffins cost $3.88\nin New York.  Please buy me two of them.\n\n Thanks.'
        returns ['Good', 'muffins', 'cost', '3.88', 'in', 'New', 'York','Please', 'buy', 'me', 'two', 'of', 'them', 'Thanks']
  '''

  #Split text into tokens
  tokens=nltk.tokenize.word_tokenize(file_text)
  final_tokens=[]
  for token in tokens:
    # Add into final_tokens after lower casing the token if it is not a punctuation symbol
    if(token not in string.punctuation):
      token=token.lower()
      final_tokens.append(token)
  return final_tokens

'''
  Document class structure:
  id:  doc ID
  doc_name: document title
  url: document url
  tf: term frequency vector for the document
 
  create() function updates the inverted index for the document
                    and populates the tf vector
'''
class document:
  def __init__(self,tag,id):
    self.id = id
    self.doc_name = tag["title"]
    self.url = tag["url"]
    self.tf = np.zeros((len(vocabulary),1))
    self.create(clean_text(tag.get_text()))

  def create(self,tokens):
    for token in tokens:
      token_id = reverse_vocabulary[token].id
      self.tf[token_id]=self.tf[token_id]+1
      if(len(inverted_index[token])!=0 and inverted_index[token][-1]==self.id):
        continue
      inverted_index[token].append(self.id)

'''
  Term class structure:
  id: id assigned to word
  word: original word
'''
class term:
  def __init__(self,id,word):
    self.id=id
    self.word=word

def create_vocab_dicts(doc_text):
  '''
  creates vocabulary and reverse-vocabulary using tokens tokens returned from clean_text function
    vocab{
      0 : term0
      1: term1
    }

    rev_vocab{
      term0.word :term0
      term1.word :term1
    }
  '''
  tokens = clean_text(doc_text)
  for token in tokens:
    if(token in reverse_vocabulary.keys()): 
      continue
    term_obj=term(len(vocabulary),token)
    vocabulary[term_obj.id]=term_obj
    reverse_vocabulary[term_obj.word]=term_obj
    inverted_index[term_obj.word]=[]

def parse_docs(f):
  '''
    Takes filename as input, extracts text from it.
    Parses the documents found into appropriate objects 
  '''

  file = open(f, "r")
  data = file.read()

  soup = bs.BeautifulSoup(data,'html.parser')
  all_doc_tags = soup.find_all('doc')

  print(str(len(all_doc_tags))+" documents found in the file.")

  # Create vocabulary for the corpus
  for each_tag in all_doc_tags:
    create_vocab_dicts(each_tag.get_text())

  #Store each document object
  for i,each_tag in enumerate(all_doc_tags):
    all_docs[i] = document(each_tag,i)

#Save files
def saveFiles(obj,fileName):
    fp = open(fileName, 'wb')
    pickle.dump(obj, fp)
    fp.close()


def main():
  if(len(sys.argv) == 2):
    filename = sys.argv[1]
  else:
    print("Please enter filename")
  
  print("\nParsing documents...")
  parse_docs(filename)
  
  print("\nSaving relevant information...")
  saveFiles(all_docs,'documents')
  saveFiles(vocabulary,'vocabulary')
  saveFiles(reverse_vocabulary,'reverse-vocabulary')
  saveFiles(inverted_index,'inverted-index')
  print("Saved!")

if __name__ == "__main__":
  main()
