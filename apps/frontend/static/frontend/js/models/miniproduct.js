define([
	'models/base'
	], function(BaseModel){

		var MiniProductModel = BaseModel.extend({
			url: '',
			save: function(attributes, options){
				options || (options = {});
				var cart = options.cart || false;
				var substitute = options.substitute || false;
				var quantity = options.quantity || 0;
				var remove = options.remove || false;
				var vent = this.vent;
				var reference = options.reference || this.toJSON().product.reference;
				var reference_selected = options.reference_selected || null;
				var osm_selected = options.osm_selected || null;
				var content_id = options.content_id || this.get('id');
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

				if (quantity<1 && !substitute) return null;


				if(substitute){
					options.type = 'POST';
					options.url = '/api/product/reference/'+reference+'/recommendations/';
					var that = this;
					options.success = function( data,  textStatus, jqXHR){
						vent.trigger('cart:newproduct');
						if (success) success(data,  textStatus, jqXHR);
					}
					options.attrs = {
						'content_id': content_id,
						'reference_selected': reference_selected,
						'osm_selected': osm_selected
					}

				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			},
			fetch: function(options){
				options = options ? _.clone(options) : {};
				var reference = options.reference || this.get('product').reference;
				options.url = '/api/product/reference/'+reference+'/recommendations/';
				return BaseModel.prototype.fetch.apply(this, [options]);
			}
		})

		return MiniProductModel;
})