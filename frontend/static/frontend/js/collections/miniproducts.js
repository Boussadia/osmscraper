define([
	'collections/base',
	'models/miniproduct'
	], function(BaseCollection, MiniProductModel){

		var MiniProductsCollection = BaseCollection.extend({
			model: MiniProductModel,
			initialize: function(models, options){
				this.suggested = options.suggested;

			}
		})

		return MiniProductsCollection;
})