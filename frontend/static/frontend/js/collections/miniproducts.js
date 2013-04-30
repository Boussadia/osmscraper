define([
	'collections/base',
	'models/miniproduct'
	], function(BaseCollection, MiniProductModel){

		var MiniProductsCollection = BaseCollection.extend({
			model: MiniProductModel
		})

		return MiniProductsCollection;
})