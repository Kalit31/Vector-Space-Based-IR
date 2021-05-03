import numpy as np
from collections import defaultdict
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup
import nltk
import pickle
from gensim import corpora, models, similarities

'''
Intialize data structures

vocabulary{
  0 : term0 
  1 : term1
}

reverse_vocabulary{
  term0.word :term0
  term1.word :term1
}

all_docs: stores all the documents found in the file

inverted_index: stores the inverted index for the corpus

corpus_text: document text list

corpus_title: list of titles of all the documents

'''
vocabulary = {}
reverse_vocabulary = {}
all_docs = {}
inverted_index = {}

corpus_text = []
corpus_title = []
dictionary = None
corpus = None


def clean_text(file_text):
	'''
		  Takes a text as input and returns a list of splitted tokens, excluding punctuations

		  eg: s='Good muffins cost $3.88\nin New York.  Please buy me two of them.\n\n Thanks.'
				  returns ['Good', 'muffins', 'cost', '3.88', 'in', 'New', 'York','Please', 'buy', 'me', 'two', 'of', 'them', 'Thanks']
	'''

	# Split text into tokens
	tokens = nltk.tokenize.word_tokenize(file_text)
	final_tokens = []
	for token in tokens:
		# Add into final_tokens after lower casing the token if it is not a punctuation symbol
		if (token not in string.punctuation):
			token = token.lower()
			final_tokens.append(token)
	return final_tokens


class document:
	'''
	Document class structure:

	Attributes
	----------

		  id:  doc ID
		  doc_name: document title
		  url: document url
		  tokens: document text splitted into tokens
		  tf: term frequency vector for the document


	Methods
	-------

		  create ( tokens ):
			create the inverted index and for the given tokens

	'''

	def __init__(self, tag, id):
		self.id = id
		self.doc_name = tag["title"]
		self.url = tag["url"]
		# self.tokens=
		self.tf = np.zeros((len(vocabulary), 1))
		self.create(clean_text(tag.get_text()))

	def create(self, tokens):
		for token in tokens:
			token_id = reverse_vocabulary[token].id
			self.tf[token_id] = self.tf[token_id]+1
			if(len(inverted_index[token]) != 0 and inverted_index[token][-1] == self.id):
				continue
			inverted_index[token].append(self.id)


class term:
	'''
			Term class structure:
			id: id assigned to word
			word: original word
	'''

	def __init__(self, id, word):
		self.id = id
		self.word = word


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
		term_obj = term(len(vocabulary), token)
		vocabulary[term_obj.id] = term_obj
		reverse_vocabulary[term_obj.word] = term_obj
		inverted_index[term_obj.word] = []


def parse_docs(f):
	'''
		  Takes filename as input, extracts text from it.
		  Parses the documents found into appropriate objects 

		  Parameters
		  ----------
			f (str) : Address of the file to be parsed
	'''

	file = open(f, "r")
	data = file.read()

	soup = bs.BeautifulSoup(data, 'html.parser')
	all_doc_tags = soup.find_all('doc')

	print(str(len(all_doc_tags))+" documents found in the file.")

	# Create vocabulary for the corpus
	for each_tag in all_doc_tags:
		create_vocab_dicts(each_tag.get_text())

	# Store each document object
	for i, each_tag in enumerate(all_doc_tags):
		all_docs[i] = document(each_tag, i)


def create_lsi_model():
	'''
		  Create an LSI model using LsiModel method from the genism package
		  ...
		  Parameters
		  ----------
			corpus (list) : list of texts of all the documents of the corpus
			dictionary (corpora.dictionary) : A corpora.dictonary of all the texts of the corpus     
		  '''
	global lsi_model, corpus_lsi
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi_model = models.LsiModel(
		corpus_tfidf, id2word=dictionary, chunksize=5000)
	corpus_lsi = lsi_model[corpus_tfidf]
	index = similarities.MatrixSimilarity(corpus_lsi)


def save_files():
	'''
		  Saves all the required files for running a test query from the created index

		  Parameters 
		  ----------

		  Takes in global values of corpus_title, corpus_lsi, dictionary, and lsi_model

	'''
	np.save('titles_improv2.npy', corpus_title)

	with open('corpus_lsi', 'wb') as corpus_lsi_file:
		pickle.dump(corpus_lsi, corpus_lsi_file)

	with open('dictionary', 'wb') as dictionary_file:
		pickle.dump(dictionary, dictionary_file)

	with open('lsi_model', 'wb') as lsi_model_file:
		pickle.dump(lsi_model, lsi_model_file)


def parser(filename):
	'''
		parser the given file into dictionary and getting the corpus

		Args
		----
			filename (str): address of the file to be parsed
	'''
	global corpus, dictionary
	file = open(filename, "r", encoding="utf8")
	soup1 = BeautifulSoup(file, 'html.parser')

	for each_tag in soup1.find_all('doc'):
		each_tag_text = each_tag.get_text()
		each_tag_title = each_tag.get('title')
		each_tag_text = each_tag_text.lower()
		each_tag_text = re.sub(r'[^\w\s]', '', each_tag_text)
		corpus_text.append(each_tag_text)
		corpus_title.append(each_tag_title)

	texts = [[word.lower() for word in document.split()]
			 for document in corpus_text]

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]


if __name__ == "__main__":

	f1 = "./../dataset/wiki_00"

	print("Parsing the document")
	parser(f1)
	print("Creating LSI model")
	create_lsi_model()
	print("Saving into files")
	save_files()
