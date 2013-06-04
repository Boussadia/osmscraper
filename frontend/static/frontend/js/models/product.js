define([
	'underscore',
	'models/base',
	],function(_, BaseModel){

		var ProductModel = BaseModel.extend({
			idAttribute: 'reference',
			urlRoot: '/api/product/reference/',
			defaults: {
				'name': 'test'
			},
			initialize: function(){
				// Getting quantity in cart
				this.vent.on('product:quantity:set', this.set_quantity, this);

			},
			save: function(attributes, options){
				options || (options = {});
				var cart = options.cart || false;
				var add = options.add || null;
				var remove = options.remove || null;
				var vent = this.vent;
				var reference = options.reference || this.id;

				if(cart){
					options.type = ( add ? 'POST' : 'DELETE' );
					options.url = '/api/cart/product/'+reference+'/quantity/1';
					var that = this;
					options.success = function( data,  textStatus, jqXHR){
						vent.trigger('cart:newproduct');
					}
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			},
			fetch: function(options){
				options = options ? _.clone(options) : {};
				var reference = options.reference || this.get('product').reference;
				options.url = '/api/product/reference/'+reference+'/recommendations/';
				return BaseModel.prototype.fetch.apply(this, [options]);
			},
			set_quantity: function(options){
				options || (options = {});

				var local_reference = this.get('reference')
				var cart_reference = options.reference;


				if(local_reference === cart_reference){
					var quantity = options.quantity || 0;
					this.set('quantity_in_cart', quantity);
				}
			},
		})

		return ProductModel;
})