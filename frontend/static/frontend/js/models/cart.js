define([
	'models/base'
	], function(BaseModel){

		var CartModel = BaseModel.extend({
			url: '/api/cart',
			parse: function(resp, xhr){
				return resp.cart;
			}
		})

		return CartModel;

})