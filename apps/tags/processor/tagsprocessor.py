#!/usr/bin/python
# -*- coding: utf-8 -*-

from dalliz.models import Category
from apps.tags.models import Tag

def diff(l1,l2):
	"""
		Compute difference between 2 lists. Returns new, common and removed items.
		Example : 
			l1 = [1,2,3]
			l2 = [1,3,4]
			ouput : new = [4], common = [1,3], removed = [2]

		Input :
			- l1 : a list
			- l2 : a list
		Ouput : 
			- new, common, removed : a tupple of 3 lists
	"""
	return list(set([t for t in l1 if t in l2]))

class TagsProcessor(object):
	"""
		Base class that sets tags for products and assigns unique dalliz category to products.
	"""

	def __init__(self, osm):
		self.osm = osm
		self.stemmed_tags = [tag.stemmed_name for tag in Tag.objects.filter(stemmed_name__isnull = False)]


	def chunk(self, text, n):
		"""
			Generates chunks of text.

			Input : 
				- text (string) : text to be chunked
				- n (int) : size of chunks
		"""
		tokens = text.split()
		return [' '.join([tokens[i+j] for j in xrange(0,n)]) for i in xrange(0,len(tokens)-n+1)]

	def reverse_get_tag(self, stemmed_name):
		"""
			Gets tag database entity from stemmed_name
		"""
		return Tag.objects.filter(stemmed_name = stemmed_name)

	def best_category_match(self, categories, retained_tags):
		if len(categories)>0:
			selected_caegory = sorted([ (category, len(diff(category.tags.all(), retained_tags))) for category in categories], key = lambda item: -item[1])[0][0]
			common_tags = diff( selected_caegory.tags.all(), retained_tags)

			return selected_caegory, common_tags
		else:
			return None, None

	def process_product(self, product):
		"""
			Process for a single product.

			Input :
				- product : osm product database entity
		"""
		chunks = [self.chunk(product.stemmed_text, n) for n in [1,2,3]]
		common = []

		[ common.extend(diff(c, self.stemmed_tags)) for c in chunks]

		retained_tags = []

		[ retained_tags.extend(self.reverse_get_tag(c)) for c in list(set(common))]

		# Now setting category :
		selected_category, final_tags = self.best_category_match(product.dalliz_category.all(), retained_tags)
		if selected_category is not None and final_tags is not None:
			product.processed = True
			product.save()

			# Cleaning and saving new relations
			product.dalliz_category.clear()
			product.tag.clear()
			product.dalliz_category.add(selected_category)
			[product.tag.add(t) for t in final_tags]
		

	def process_category(self, id_category, overwrite = False):
		"""
			Processing all products from dalliz id_category
		"""
		category = Category.objects.get(id = id_category)
		osm_categories = getattr(category, self.osm+'_category_dalliz_category').all()
		for osm_category in osm_categories:
			products = osm_category.product_set.filter(stemmed_text__isnull = False)
			if not overwrite:
				products.filter(processed = False)
			for product in products:
				self.process_product(product)



