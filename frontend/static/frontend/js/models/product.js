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

				if(cart){
					options.type = ( add ? 'POST' : 'DELETE' );
					options.url = '/api/cart/product/'+this.id+'/quantity/1';
					var that = this;
					options.success = function( data,  textStatus, jqXHR){
						if( typeof data.attributes.carts !== 'undefined' && typeof vent !== 'undefined') vent.trigger('carts', data.attributes.carts);
						// if( typeof data.attributes.osm !== 'undefined' && typeof vent !== 'undefined') vent.trigger('osm', data.attributes.osm);
						vent.trigger('cart:newproduct');
					}
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			},
			set_quantity: function(options){
				options || (options.reference);

				var local_reference = this.get('reference')
				var cart_reference = options.reference;


				if(local_reference === cart_reference){
					var quantity = options.quantity || 0;
					this.set('quantity_in_cart', quantity);
				}
			}
		})

		return ProductModel;
})