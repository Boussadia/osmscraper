define([
	'underscore',
	'models/base',
	],function(_, BaseModel){

		var ProductModel = BaseModel.extend({
			idAttribute: 'reference',
			urlRoot: '/api/product/reference/',
			defaults: {
				'name': 'test',
				'content_id': null
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
				var content_id = options.content_id || this.get('content_id');
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

				options.attrs = {
					'content_id': content_id
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

				var local_reference = this.get('reference');

				if ( local_reference in options){
					var content_id = options[local_reference].content_id || null;
					var quantity = options[local_reference].quantity;
					this.set('quantity_in_cart', quantity);
					this.set('content_id', content_id);
				}else{
					this.set('quantity_in_cart', 0);
					this.set('content_id', null);
				}
			},
			cart_empty: function(options){
				this.set('quantity_in_cart', 0);
			}
		})

		return ProductModel;
})