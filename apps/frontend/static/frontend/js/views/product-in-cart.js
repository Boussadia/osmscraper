define([
	'underscore',
	'views/product',
	'text!../../templates/product-in-cart.html'
], function(_, ProductView, productTemplate){


	var ProductInCartView = ProductView.extend({
		template: _.template(productTemplate),
		events: {
			'click a.add-cart': 'addToCart',
			'click a.plus': 'addToCart',
			'click a.minus': 'removeFromCart',
			'click .unavailable-mask div': 'showSubstitution',
		},
		showSubstitution: function(e){
			this.vent.trigger('product:recomandation', this.product);
		}
	});

	return ProductInCartView;
})