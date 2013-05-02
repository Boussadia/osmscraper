define([
	'models/base',
	'collections/products'
	], function(BaseModel, ProductsCollection){

		var CategoryModel = BaseModel.extend({
			initialize: function(attributes, options){
				options || (options = {});
				if (attributes.name === 'promotions'){
					var type = 'promotions';
				}else{
					var type = 'products';
				}
				this.products = new ProductsCollection([], {'category_id':this.get('id'), 'type': type, 'vent': this.vent});
			},
			fetch_products: function(options){
				this.products.fetch(options);
			}

		});

		return CategoryModel;
})