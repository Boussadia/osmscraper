define([
	'underscore',
	'models/base'
	], function(_, BaseModel){

		var CartModel = BaseModel.extend({
			url: '/api/cart',
			defaults:{
				'quantity': 0,
			},
			initialize: function(attributes, options){
				this.osms = options.osms;
				this.set_suggested();
				this.vent.on('cart:newproduct', this.fetch, this);
				this.on('change',  this.check_quantity, this);

				this.osms.on('change add', function(osm){
					if(osm.get('active') &&  this.get('name') !== osm.get('name')){
						this.set('name', osm.get('name'));
						this.set_suggested();
						this.fetch();
					}else if(!osm.get('active') &&  this.get('name') === this.suggested){
						this.set_suggested(osm.get('name'))

					}
				}, this);

				// Messages for products quantity
				this.vent.on('request:products:quantity', this.check_quantity, this);
				
			},
			parse: function(resp, xhr){
				return resp;
			},
			set_suggested: function(suggested){
				if(!suggested){
					var unactive_osm = this.osms.find(function(osm){
						return !osm.get('active');
					});
					if (unactive_osm) this.suggested =  unactive_osm.get('name') || 'monoprix';
					if (!unactive_osm) this.suggested =  'monoprix';

				}else{
					this.suggested = suggested;
				}

				if (this.suggested === this.get('name')) this.set_suggested();
			},
			check_quantity: function(model, options){
				var content = this.toJSON().content;
				var to_send = {}
				_.each(content, function(category){
					var products = category.products;
					_.each(products, function(product){
						var reference = product.product.reference;
						var quantity = product.quantity;
						to_send[reference] = quantity;
					}, this);
				}, this);

				_.each(to_send, function(quantity,reference){
					var option_to_send = {
						'reference': reference,
						'quantity': quantity
					}

					this.vent.trigger('product:quantity:set', option_to_send);
				},this)
			}
		})

		return CartModel;

})