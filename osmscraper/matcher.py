#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import math

"""
	In this file there is the base class for the algorithm that perform matching of products
	Using the Vector model representation of a document to perform matching of brand with a product title from telemarket.
	We are using the TF-IDF ponderation of a term inide a document of a corpus.
	The corpus of document is the title of products extracted from the database.
"""

REGEXP = re.compile(r'\W')

class Matcher(object):
	"""
		Base matcher class that performs algorithm that matches products together.

		Init:
			- corpus (dict):
				{
					"id": (int) id of element,
					"content": (string) content of the document.

				}
	"""
	def __init__(self, corpus):
		super(Matcher, self).__init__()
		self.__corpus__ = corpus
		self.__tokens__ = {}
		self.__index__ = {}
		self.__possible_matches__ = {} # possible matches for queries
		self.__matches__ = {} # definitive matches for queries (after decision process)


	def get_corpus(self):
		return self.__corpus__

	def get_tokens(self):
		return self.__tokens__

	def get_index(self):
		return self.__index__

	def set_tokens(self,tokens):
		self.__tokens__ = tokens

	def set_index(self,index):
		self.__index__ = index

	def get_possible_matches(self, query = None):
		if query is None:
			return self.__possible_matches__
		else:
			if query in self.__possible_matches__.iterkeys():
				return self.__possible_matches__[query]
			else:
				self.process_query(query)				
				return self.__possible_matches__[query]

	def set_possible_matches(self, query, possible_matches):
		self.__possible_matches__[query] = possible_matches

	@staticmethod
	def get_histogram(word):
		hist = {}
		for s in word:
			if s in hist.iterkeys():
				hist[s] += 1.0
			else:
				hist[s] = 1.0
		return hist

	@staticmethod
	def get_norm(histogram):
		return math.sqrt(sum( [ v**2 for s,v in histogram.iteritems() ] ))

	@staticmethod
	def get_similarity(word_1, word_2):
		# if word_1 == word_2:
		# 	return 1.0
		# elif word_2 == "" or word_1 == "":
		# 	return 0.0
		# else:
		# 	hist_1 = Matcher.get_histogram(word_1)
		# 	hist_2 = Matcher.get_histogram(word_2)
		# 	norm_1 = Matcher.get_norm(hist_1)
		# 	norm_2 = Matcher.get_norm(hist_2)

		# 	score = 0.0

		# 	for s, v in hist_1.iteritems():
		# 		if s in hist_2.iterkeys():
		# 			score += v*hist_2[s]

		# 	return score /(norm_1*norm_2)

		return math.exp(-(1.0/1.0)*Matcher.levenshtein(word_1, word_2)**(2.0))

	@staticmethod
	def levenshtein(s1, s2):
		if len(s1) < len(s2):
			return Matcher.levenshtein(s2, s1)
		if not s1:
			return len(s2)

		previous_row = xrange(len(s2) +1)
		for i, c1 in enumerate(s1):
			current_row = [i + 1]
			for j, c2 in enumerate(s2):
				insertions = previous_row[j + 1] + 1.0 # j+1 instead of j since previous_row and current_row are one character longer
				deletions = current_row[j]      # than s2
				substitutions = previous_row[j] + (c1 != c2)
				current_row.append(min(insertions, deletions, substitutions))
			previous_row = current_row

		return previous_row[-1]

	@staticmethod
	def generate_TF(word, terms):
		score = 0.0
		if word in terms:
			# score += Matcher.get_similarity(term, word)
			score += 1
		return score / len(terms)

	@staticmethod
	def generate_TFS(text):
		terms = REGEXP.split(text)
		TFS = {}

		for i in xrange(0,len(terms)):
			term = terms[i]
			if term in TFS.iterkeys():
				TFS[term] += Matcher.generate_TF(term, terms)
			else:
				TFS[term] = Matcher.generate_TF(term, terms)

		return TFS

	@staticmethod
	def get_IDF(word, index):
		if word in index.iterkeys():
			return index[word]["idf"]
		else:
			return 0.0

	def tokenize(self):
		self.set_index({})
		index = {}
		documents = self.get_corpus()
		print "Building index for corpus of "+str(len(documents))+" documents"

		# Calculating TF
		for i in xrange(0,len(documents)):
			name = documents[i]["content"]
			tfs = Matcher.generate_TFS(name)
			documents[i]["tfs"] = tfs

			# Adding terms to base vector
			for term, tf in tfs.iteritems():
				if term not in index.iterkeys():
					index[term] = {"frequency_corpus":  1}
				else:
					index[term]["frequency_corpus"] += 1

		# Calculating IDF
		for term in index.iterkeys():
			index[term]['idf'] = math.log(len(documents)/(1.0+index[term]["frequency_corpus"]))

		# Calculating norm of each document
		for i in xrange(0,len(documents)):
			# Problem with 
			documents[i]['norm'] = 0
			for word, tf in documents[i]["tfs"].iteritems():
				tfidf_base_term = tf*index[word]['idf']
				documents[i]['norm'] += tfidf_base_term**2

			documents[i]['norm'] = math.sqrt(documents[i]['norm'])

		self.set_index(index)
		self.set_tokens(documents)

	@staticmethod
	def get_TFIDF(text, index):
		idfs = {}
		tfs = Matcher.generate_TFS(text)

		for word, tf in tfs.iteritems():
			idf = Matcher.get_IDF(word, index)
			idfs[word] = idf

		return tfs, idfs, index

	@staticmethod
	def generate_score(text, document, index ):
		score = 0.0
		# tfs, idfs, index = Matcher.get_TFIDF(text, index)

		# norm_text = math.sqrt(sum( [ (idf*tfs[word])**2 for word, idf in idfs.iteritems()]))

		# if norm_text>0:
		# 	for word, tf in tfs.iteritems():
		# 		if word in document["tfs"].iterkeys():
		# 			score += document["tfs"][word]*index[word]['idf']*tf*idfs[word]
		# 		else:
		# 			if 'similarity_word' in index[word].iterkeys():
		# 				similarity_word = index[word]['similarity_word']
		# 				if similarity_word in document["tfs"].iterkeys():
		# 					score += document["tfs"][similarity_word]*index[similarity_word]['idf']*tf*idfs[word]
		# 			else:
		# 				# Looking for word with biggest similarity
		# 				max_similarity = 0.0
		# 				word_similarity = ''
		# 				for document_word in document["tfs"].iterkeys():
		# 					score_similarity = Matcher.get_similarity(document_word, word)
		# 					if score_similarity > max_similarity:
		# 						max_similarity = score_similarity
		# 						word_similarity = document_word

		# 				score += document["tfs"][word_similarity]*index[word_similarity]['idf']*tf*idfs[word]*score_similarity


			
		# 	score = score/(norm_text*document['norm'])

		# Matricial calculation
		words = REGEXP.split(text)
		norm_text = 0
		norm_doc = 0

		words_similarity = {}
		for word in words:
			if word in document["tfs"].iterkeys():
				words_similarity[word] = {"word":word, "similarity": 1.0}
			else:
				words_similarity[word] = {"word":word, "similarity": 0.0}
				for base_term in document["tfs"].iterkeys():
					similarity = Matcher.get_similarity(base_term, word)
					if similarity>words_similarity[word]["similarity"]:
						words_similarity[word] = {"word":base_term, "similarity": similarity}

		# print words_similarity

		for word in words_similarity.iterkeys():
			base_term = words_similarity[word]["word"]
			similarity = words_similarity[word]["similarity"]
			tfidf_base_term = document["tfs"][base_term]*index[base_term]['idf']
			# print str(similarity)+' btw '+base_term+' and '+word+' tfidf : '+str(tfidf_base_term)
			score += (tfidf_base_term*similarity)*tfidf_base_term
			norm_text += (tfidf_base_term*similarity)**2
			norm_doc += tfidf_base_term**2

		# print score
		norm_text = math.sqrt(norm_text)
		norm_doc = math.sqrt(norm_doc)
		score = score/(norm_text*norm_doc)

		# print norm_text
		# print norm_doc
		# print document['norm']

		return score, index

	@staticmethod
	def get_norm_matrix(matrix):
		norm = 0.0
		size = len(matrix[0])
		vector = [ 0 for i in xrange(0,size) ]

		for i in xrange(0,size):
			vector[i] = sum( ( base_vector[i]**2 for base_vector in matrix ) )

		return math.sqrt( sum( val for val in vector) )


	def process_query(self, query):
		print "Calculating score for "+query
		possible_matches = []

		documents = self.get_tokens()
		index = self.get_index()

		for i in xrange(0,len(documents)):
			score, index = Matcher.generate_score(query, documents[i], index)
			if score > 0:
				possible_matches.append({"id": documents[i]["id"], "score": score})

		self.set_index(index)
		self.set_possible_matches(query, possible_matches)

	def process_queries(self, queries):
		for i in xrange(0, len(queries)):
			query = queries[i]
			self.process_query(query)

	def get_token(self, id):
		token = None
		tokens = self.get_tokens()
		for i in xrange(0,len(tokens)):
			if tokens[i]['id'] == id:
				token =tokens[i]
				break
		return token

	def print_matches(self, query, threshold = 0):
		possible_matches = self.get_possible_matches(query)
		for i in xrange(1,len(possible_matches)):
			token = self.get_token(id=possible_matches[i]['id'])
			if possible_matches[i]['score'] > threshold:
				print 'Content : '+token['content']+' -> '+str(possible_matches[i]['score'])



