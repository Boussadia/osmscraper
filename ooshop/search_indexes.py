from haystack import indexes

from ooshop.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	# brand = indexes.CharField(model_attr = 'brand')


	def get_model(self):
		return Product

	def index_queryset(self, using = None):
		"""
			Used when the entire index for model is updated.
		"""
		return self.get_model().objects.filter(exists = True)
