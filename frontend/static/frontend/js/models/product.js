define([
	'models/base',
	],function(BaseModel){

		var ProductModel = BaseModel.extend({
			default: {
				'name': 'test'
			}
		})

		return ProductModel;
})