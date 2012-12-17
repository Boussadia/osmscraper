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
STOP_WORDS = ['l','g','cl','et','d','kg','de', 'au', 'a', 'les', 'la']

class Engine(object):
	"""
		Base engine class that performs algorithm that matches products together.

		Init:
			- corpus (dict):
				{
					"id": (int) id of element,
					"content": (string) content of the document.

				}
	"""
	def __init__(self, corpus):
		super(Engine, self).__init__()
		self.__corpus__ = corpus
		self.__tokens__ = {}
		self.__index__ = {}
		self.__possible_matches__ = {} # possible matches for queries
		self.__similarities__ = {}

	@staticmethod
	def remove_stop_words( text):
		terms = REGEXP.split(text)
		clean_terms = []
		while len(terms)>0:
			if terms[0] in STOP_WORDS:
				terms.pop(0)
			else:
				clean_terms.append(terms.pop(0))

		return clean_terms

	def add_similarity_word(self, word, base_word, similarity):
		self.__similarities__[word] = {"word":base_word, "similarity":similarity}

	def get_similarity_word(self, word):
		if word in self.__similarities__:
			return self.__similarities__[word]
		else:
			return None

	def get_corpus(self):
		for i in xrange(0, len(self.__corpus__)):
			yield self.__corpus__[i]

	def get_tokens(self):
		for i in xrange(0, len(self.__tokens__)):
			yield self.__tokens__[i]

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
		return math.sqrt(sum( ( float(v)**2 for s,v in histogram.iteritems() ) ))

	@staticmethod
	def get_similarity(word_1, word_2):
		len_word_1 = len(word_1)
		len_word_2 = len(word_2)
		max_len = max(len_word_1, len_word_2)
		if max_len == 0:
			return 0
		elif abs(len_word_1-len_word_2)/max_len>.1:
			return 0 
		else:
			# hist_1 = Engine.get_histogram(word_1)
			# hist_2 = Engine.get_histogram(word_2)
			# norm_1 = Engine.get_norm(hist_1)
			# norm_2 = Engine.get_norm(hist_2)

			# if norm_2*norm_1>0:

			# 	score = 0.0

			# 	for char_1, f_1 in hist_1.iteritems():
			# 		if char_1 in hist_2.iterkeys():
			# 			score += f_1*hist_2[char_1]

			# 	return score/(norm_1*norm_2)
			# else:
			# 	return 0.0
			return math.exp(-(1.0/1.0)*Engine.levenshtein(word_1, word_2)**(2.0))

	@staticmethod
	def levenshtein(s1, s2):
		if len(s1) < len(s2):
			return Engine.levenshtein(s2, s1)
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
			# score += Engine.get_similarity(term, word)
			score += 1
		return score / len(terms)

	@staticmethod
	def generate_TFS(text):
		terms = Engine.remove_stop_words(text)
		TFS = {}

		for i in xrange(0,len(terms)):
			term = terms[i]
			if term in TFS.iterkeys():
				TFS[term] += Engine.generate_TF(term, terms)
			else:
				TFS[term] = Engine.generate_TF(term, terms)

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
		tokens = []
		print "Building index for corpus"
		nb_documents = 0

		# Calculating TF
		for document in documents:
			nb_documents += 1
			name = document["content"]
			tfs = Engine.generate_TFS(name)
			document["tfs"] = tfs
			tokens.append(document)

			# Adding terms to base vector
			for term, tf in tfs.iteritems():
				if term not in index.iterkeys():
					index[term] = {"frequency_corpus":  1}
				else:
					index[term]["frequency_corpus"] += 1

		# Calculating IDF
		for term in index.iterkeys():
			index[term]['idf'] = math.log(nb_documents/(1.0+index[term]["frequency_corpus"]))

		self.set_index(index)
		self.set_tokens(tokens)

	@staticmethod
	def get_TFIDF(text, index):
		idfs = {}
		tfs = Engine.generate_TFS(text)

		for word, tf in tfs.iteritems():
			idf = Engine.get_IDF(word, index)
			idfs[word] = idf

		return tfs, idfs, index

	def generate_score(self, text, document ):
		score = 0.0
		words = Engine.remove_stop_words(text)
		index = self.get_index()
		norm_text = 0
		norm_doc = 0

		words_similarity = {}

		for word in words:
			if word in index.iterkeys():
				words_similarity[word] = {"word":word, "similarity": 1.0}
			else:
				dict_similarity = self.get_similarity_word(word)
				if dict_similarity is None:
					words_similarity[word] = {"word":word, "similarity": 0.0}
					for base_term in index.iterkeys():
						similarity = Engine.get_similarity(base_term, word)
						if similarity>words_similarity[word]["similarity"]:
							words_similarity[word] = {"word":base_term, "similarity": similarity}

					if words_similarity[word]["word"] in index.iterkeys():
						self.add_similarity_word(word, words_similarity[word]["word"], words_similarity[word]["similarity"])
				else:
					words_similarity[word] = {"word":dict_similarity['word'], "similarity": dict_similarity['similarity']}

		tfidfs = {}
		for word in document['tfs'].iterkeys():
			tfidfs[word] = document["tfs"][word]*index[word]['idf']
			norm_doc += tfidfs[word]**2

		for word in words_similarity.iterkeys():
			base_term = words_similarity[word]["word"]
			similarity = words_similarity[word]["similarity"]
			if base_term in document["tfs"].iterkeys():
				tfidf_base_term =tfidfs[base_term]
			else:
				tfidf_base_term = 0
			# print str(similarity)+' btw '+base_term+' and '+word+' tfidf : '+str(tfidf_base_term)
			score += (tfidf_base_term*similarity)*tfidf_base_term
			norm_text += (tfidf_base_term*similarity)**2

		norm_text = math.sqrt(norm_text)
		norm_doc = math.sqrt(norm_doc)
		# print score
		# print norm_text
		# print norm_doc
		# print ''
		if norm_text*norm_doc>0 and score>0.01:
			score = score/(norm_text*norm_doc)
		else:
			score = 0

		self.set_index(index)
		return score

	def process_query(self, query):
		print "Calculating score for "+query
		possible_matches = []

		documents = self.get_tokens()

		for document in documents:
			score = self.generate_score(query, document)
			if score > 0:
				possible_matches.append({"id": document["id"], "score": score})
				# print '\tScore for '+document['content']+' -> '+str(score)

		self.set_possible_matches(query, possible_matches)

	def process_queries(self, queries):
		for i in xrange(0, len(queries)):
			query = queries[i]
			self.process_query(query)

	def get_token(self, id):
		tokens = self.get_tokens()
		for token in tokens:
			if token['id'] == id:
				return token
				break
		return None

	def print_matches(self, query, threshold = 0):
		possible_matches = self.get_possible_matches(query)
		for i in xrange(1,len(possible_matches)):
			token = self.get_token(id=possible_matches[i]['id'])
			if possible_matches[i]['score'] > threshold:
				print 'Content : '+token['content']+' -> '+str(possible_matches[i]['score'])

	def are_comprable(self, document_1, document_2):
		"""
			In order to use this method, create a child class and overide default behavior
		"""
		return True

class Product_engine(Engine):
	def __init__(self, corpus):
		super(Product_engine, self).__init__(corpus)

	def are_comprable(self, product_1, product_2, brand = False):
		"""
			Comparaison of products compared by unit of product. if brand is set to True, takes intot acount brand of product.
		"""
		if product_1["unit"] == product_2["unit"]:
			for i in xrange(0,len(product_1['categories'])):
				for j in xrange(0,len(product_2['categories'])):
					if product_1['categories'][i] == product_2['categories'][j]:
						if brand:
							for k in xrange(0, len(product_1['brands'])):
								for l in xrange(0, len(product_2['brands'])):
									if product_1['brands'][k] == product_2['brands'][l]:
										return True
						else:
							return True

		return False

	def set_possible_products(self, product_dict, brand = False):
		"""
			Sets possible matches for a product, if brand is true, takes into account for product brand.
		"""
		query = product_dict['content']
		print "Calculating score for "+product_dict['content']
		possible_matches = []

		products = self.get_tokens()
		index = self.get_index()

		for product in products:
			if self.are_comprable(product_dict, product, brand):
				score = self.generate_score(query, product)
			else:
				score = 0.0
			if score > 0:
				possible_matches.append({"id": product["id"], "score": score})

		self.set_index(index)
		self.set_possible_matches(query, possible_matches)
