define([
	'models/base',
	],function(BaseModel){

		var ProductModel = BaseModel.extend({
			default:{
				'name': 'Test'
			},
			initialize: function(){}
		})

		return ProductModel;
})