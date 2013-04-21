define([
	'models/base',
	'collections/products'
	], function(BaseModel, ProductsCollection){

		var CategoryModel = BaseModel.extend({
			initialize: function(){
				this.products = new ProductsCollection({'category_id':this.get('id'), 'vent': this.vent});
			},
			fetch_products: function(){
				this.products.fetch();
			}

		});

		return CategoryModel;
})