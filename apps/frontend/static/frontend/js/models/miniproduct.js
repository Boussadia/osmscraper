define([
	'models/base'
	], function(BaseModel){

		var MiniProductModel = BaseModel.extend({
			url: '',
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
						vent.trigger('cart:newproduct');
					}
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			},
			fetch: function(options){
				options = options ? _.clone(options) : {};
				var reference = this.get('product').reference;
				options.url = '/api/product/reference/'+reference+'/recommendations/';
				return BaseModel.prototype.fetch.apply(this, [options]);;
			}
		})

		return MiniProductModel;
})