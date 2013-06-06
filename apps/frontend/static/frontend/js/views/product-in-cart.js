define([
	'underscore',
	'views/product',
	'text!../../templates/product-in-cart.html'
], function(_, ProductView, productTemplate){


	var ProductInCartView = ProductView.extend({
		template: _.template(productTemplate),
		events: {
			'click a.plus': 'addToCart',
			'click a.minus': 'removeFromCart',
			'click .unavailable-mask div': 'showSubstitution',
		},
		addToCart: function(e, delayed){
			if(typeof delayed === 'undefined' ) delayed = false;
			var reference = this.product.toJSON().product.reference;
			var quantity = this.product.get('quantity');
			return ProductView.prototype.addToCart.apply(this, [e, delayed, {'reference': reference, 'quantity': quantity}]);
		},
		removeFromCart: function(e, delayed){
			if(typeof delayed === 'undefined' ) delayed = false;
			var reference = this.product.toJSON().product.reference;
			var quantity = this.product.get('quantity');
			return ProductView.prototype.removeFromCart.apply(this, [e, delayed, {'reference': reference, 'quantity': quantity}]);
		},
		showSubstitution: function(e){
			this.vent.trigger('product:recomandation', this.product);
		}
	});

	return ProductInCartView;
})