#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time

from dalliz.models import Category
from auchan.models import Product as AuchanProduct
from monoprix.models import Product as MonoprixProduct
from ooshop.models import Product as OoshopProduct
from apps.matcher.models import ProductMatch
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
	removed = [t for t in l1 if t not in l2]
	new = [t for t in l2 if t not in l1]
	common = [t for t in l1 if t in l2]
	return new, common,removed

class TagsProcessor(object):
	"""
		Base class that sets tags for products and assigns unique dalliz category to products.
	"""
	OSMS = ['auchan', 'monoprix', 'ooshop']
	STEMMED_TAGS = [tag.stemmed_name for tag in Tag.objects.filter(stemmed_name__isnull = False)]

	def __init__(self, osm = 'monoprix'):
		self.osm = osm

	@staticmethod
	def chunk(text, n):
		"""
			Generates chunks of text.

			Input : 
				- text (string) : text to be chunked
				- n (int) : size of chunks
		"""
		if text:
			tokens = text.split()
			return [' '.join([tokens[i+j] for j in xrange(0,n)]) for i in xrange(0,len(tokens)-n+1)]
		else:
			return []

	@staticmethod
	def reverse_get_tag(stemmed_name):
		"""
			Gets tag database entity from stemmed_name
		"""
		return Tag.objects.filter(stemmed_name = stemmed_name)

	def best_category_match(self, categories, retained_tags):
		if len(categories)>0:
			new, common, removed = diff(category.tags.all(), retained_tags) 
			selected_caegory = sorted([ (category, len(common)) for category in categories], key = lambda item: -item[1])[0][0]
			new_tags, common_tags, removed_tags = diff( selected_caegory.tags.all(), retained_tags)

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

		[ common.extend(diff(c, self.stemmed_tags)[1]) for c in chunks]

		retained_tags = []

		[ retained_tags.extend(TagsProcessor.reverse_get_tag(c)) for c in list(set(common))]

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



	####################################################################################################
	#
	#								Static methods approach
	#
	####################################################################################################

	@staticmethod
	def process_tags_product(product):
		"""
			This static method sets tags to product
		"""
		chunks = [TagsProcessor.chunk(product.stemmed_text, n) for n in [1,2,3]]
		common = []

		[ common.extend(diff(c, TagsProcessor.STEMMED_TAGS)[1]) for c in chunks]

		retained_tags = []

		[ retained_tags.extend(TagsProcessor.reverse_get_tag(c)) for c in list(set(common))]

		# Cleaning and saving new relations
		product.tag.clear()
		Through = product.__class__.tag.through
		Through.objects.bulk_create([ Through(product_id=product.pk, tag_id=t.pk) for t in retained_tags ])

		product.tags_processed = True
		product.save()

		# Processing matched products
		TagsProcessor.process_matched_products(product)

	@staticmethod
	def get_best_category_match(product):
		"""
			Apply this to tags processed product.
		"""
		categories = []
		[ [categories.append(c) for c in category.dalliz_category.all()]for category in product.categories.all()]
		categories = list(set(categories))
		
		tags = product.tag.all()

		if len(categories)>0:
			selected_caegory = sorted([ (category, len(diff(category.tags.all(), tags)[1])) for category in categories], key = lambda item: -item[1])[0][0]
			new_tags, common_tags, removed_tags = diff( selected_caegory.tags.all(), tags)
			# return selected_caegory, common_tags

			# saving product
			return selected_caegory, common_tags
		else:
			return None, None

	@staticmethod
	def process_matched_products(product):
		"""
			This method merges matched product tags.
		"""
		matched_products = [product]
		possible_categories = []
		product_match = product.productmatch_set.all()
		if not product.tags_processed:
			TagsProcessor.process_tags_product(product)
		tags = list(product.tag.all())

		if product_match.count()>0:
			product_match = product_match[0]
			for osm in TagsProcessor.OSMS:
				matched_product = getattr(product_match, '%s_product'%osm)
				if matched_product and matched_product != product:
					matched_products.append(matched_product)
					if not matched_product.tags_processed:
						TagsProcessor.process_tags_product(matched_product)

					tags = tags + list(matched_product.tag.all())



			# Getting unique tags
			tags = list(set(tags))
			for p in matched_products:
				new, common, removed = diff( list(p.tag.all()), tags)

				[p.tag.add(t) for t in new]
				[p.tag.remove(t) for t in removed]

			# Working with categories
			for p in matched_products:
				possible_category, common_tags = TagsProcessor.get_best_category_match(p)
				possible_categories.append(possible_category)


			# unique category
			possible_categories = list(set(possible_categories))

			# Setting Dalliz_category to matched products
			for p in matched_products:
				p.dalliz_category.clear()
				[p.dalliz_category.add(c) for c in possible_categories]





	@staticmethod
	def process_tags_products(override = True):
		"""
			Process all categories from all 
		"""
		# Get variables in global scope
		global_keys = globals()

		# cycle trough all osms, and attribute tags to products (regardless of matches)
		for osm in TagsProcessor.OSMS:
			t0 = time()
			print 'Start %s'%(osm)
			OSMProduct = global_keys['%sProduct'%osm.capitalize()]
			kwargs = {
				'categories__dalliz_category__algorithm_process': True,
				'tags_processed': False
			}

			products = OSMProduct.objects.filter(**kwargs).distinct('reference')
			[ TagsProcessor.process_tags_product(p) for p in products]

			print time()-t0

	# @staticmethod
	# def process_categories_products():
	# 	# Get variables in global scope
	# 	global_keys = globals()

	# 	# cycle trough all osms, and attribute tags to products (regardless of matches)
	# 	for osm in TagsProcessor.OSMS:
	# 		t0 = time()
	# 		print 'Start %s'%(osm)
	# 		OSMProduct = global_keys['%sProduct'%osm.capitalize()]
	# 		kwargs = {
	# 			'categories__dalliz_category__algorithm_process': True,
	# 			'tags_processed': True,
	# 		}

	# 		products = OSMProduct.objects.filter(**kwargs).distinct('reference')
	# 		[ TagsProcessor.set_best_category_match(p) for p in products]

	# 		print time()-t0



