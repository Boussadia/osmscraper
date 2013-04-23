define([
	'collections/base',
	'models/product'
	],
	function(BaseCollection, ProductModel){

		var ProductsCollections = BaseCollection.extend({
			model: ProductModel,
			url:function(){
				return '/api/categories/id/'+this.id+'/products/top';
			},
			initialize: function(models, options){
				options || (options = {})
				var category_id = options.category_id || null;
				this.id = category_id;

			},
			parse: function(resp, xhr){
				this.name = resp.category.name;
				return resp.products;
			}
		})



		return ProductsCollections;
})