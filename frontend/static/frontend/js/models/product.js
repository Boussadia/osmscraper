define([
	'models/base',
	],function(BaseModel){

		var ProductModel = BaseModel.extend({
			defaults: {
				'name': 'test'
			}
		})

		return ProductModel;
})