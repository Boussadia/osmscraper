define([
	'underscore',
	'views/product',
	'text!../../templates/product-in-cart.html'
], function(_, ProductView, productTemplate){


	var ProductInCartView = ProductView.extend({
		template: _.template(productTemplate),
		render: function(){
			// Only render if associated product was fetched from server
			try{
				this.$el.empty();
				var data = this.product.toJSON();
				if (data.name.length > this.MAX_NAME_LENGTH){
					data.name = data.name.substring(0, this.MAX_NAME_LENGTH-3)+'...';
				}
				this.$el.append(this.template(data));
			}catch(e){}
			return this;
		},
		addToCart: function(){
			var quantity = this.product.get('quantity');
			this.product.set('quantity', quantity + 1);
			this.product.save(null, {'cart': true, 'add': 1, 'vent': this.vent, 'reference': this.product.toJSON().product.reference});
		},
		removeFromCart: function(){
			var quantity = this.product.get('quantity');
			if (quantity-1>=0){
				this.product.set('quantity', quantity - 1);
				this.product.save(null, {'cart': true, 'remove': 1, 'vent': this.vent, 'reference': this.product.toJSON().product.reference});
				this.vent.trigger('product:quantity:set', {
					'reference': this.product.toJSON().product.reference,
					'quantity': this.product.get('quantity')
				})
			}

		}
	});

	return ProductInCartView;
})