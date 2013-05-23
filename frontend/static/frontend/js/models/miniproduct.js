define([
	'models/base'
	], function(BaseModel){

		var MiniProductModel = BaseModel.extend({
			save: function(attributes, options){
				options || (options = {});
				var cart = options.cart || false;
				var add = options.add || null;
				var remove = options.remove || null;
				var vent = this.vent;

				if(cart){
					options.type = ( add ? 'POST' : 'DELETE' );
					options.url = '/api/cart/product/'+this.attributes.product.reference+'/quantity/1';
					var that = this;
					options.success = function( data,  textStatus, jqXHR){
						// if( typeof data.attributes.carts !== 'undefined') vent.trigger('carts', data.attributes.carts);
						// if( typeof data.attributes.osm !== 'undefined') vent.trigger('osm', data.attributes.osm);
						vent.trigger('cart:newproduct');
					}
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		})

		return MiniProductModel;
})