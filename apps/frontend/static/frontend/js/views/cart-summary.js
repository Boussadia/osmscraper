define([
	'underscore',
	'views/base',
	'text!../../templates/cart-summary.html'
], function(_, BaseView, cartSummaryTemplate){

	var CartSummaryView = BaseView.extend({
		template: _.template(cartSummaryTemplate),
		initialize: function(options){
			this.cart = options.cart;
			this.bindTo(this.cart, 'change', this.render);
			 
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var data = {};
			data = this.cart.toJSON();
			this.$el.append(this.template(data));
			return this;
		},
		events: {
			'click a': 'showOrHide'
		},
		showOrHide: function(){
			var className = 'open-cart';
			var $controller = this.$el.find('.controller');
			if ($controller.hasClass(className)){
				$controller.removeClass(className);
				this.vent.trigger('hide:panier');
			}else{
				$controller.addClass(className);
				this.vent.trigger('show:panier');
			}
		}
	});

	return CartSummaryView;

});