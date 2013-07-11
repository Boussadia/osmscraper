from haystack import indexes

from dalliz.models import Brand

class BrandIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, model_attr='name')
	osm = indexes.CharField(default='dalliz')

	# autocomplete for name
	name_auto = indexes.EdgeNgramField(model_attr='name', default = '')

	def get_model(self):
		return Brand

	def index_queryset(self, using = None):
		"""
			Used when the entire index for model is updated.
		"""
		return self.get_model().objects.all()
