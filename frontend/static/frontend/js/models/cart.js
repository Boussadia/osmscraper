define([
	'models/base'
	], function(BaseModel){

		var CartModel = BaseModel.extend({
			url: '/api/cart',
			initialize: function(attributes, options){
				this.vent.on('cart:newproduct', this.fetch, this);
			},
			parse: function(resp, xhr){
				return resp.cart;
			}
		})

		return CartModel;

})