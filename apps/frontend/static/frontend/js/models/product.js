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
				this.vent.on('cart:empty', this.cart_empty, this);

			},
			save: function(attributes, options){
				options || (options = {});
				var cart = options.cart || false;
				var quantity = options.quantity || 0;
				var remove = options.remove || false;
				var vent = this.vent;
				var reference = options.reference || this.id;
				var success = options.success;

				if(cart){
					options.type = ( !remove  ? 'POST' : 'DELETE' );
					options.url = '/api/cart/product/'+reference+'/quantity/'+quantity;
					var that = this;
					options.success = function( data,  textStatus, jqXHR){
						vent.trigger('cart:newproduct');
						if (success) success(data,  textStatus, jqXHR);
					}
				}

				if (quantity<1) return null;

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
			cart_empty: function(options){
				this.set('quantity_in_cart', 0);
			}
		})

		return ProductModel;
})