define([
	'collections/base',
	'models/product'
], function(BaseCollection, ProductModel){

	var SearchResults = BaseCollection.extend({
		model: ProductModel,
	})

	return SearchResults;

})