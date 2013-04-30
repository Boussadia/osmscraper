define([
	'underscore',
	'collections/miniproducts',
	'models/cart',
	'views/base',
	'views/category-in-cart',
	'views/mini-products',
	'text!../../templates/cart.html'
	], function(_, MiniProductsCollection, CartModel, BaseView, CategoryInCartView, MiniProductsView, cartTemplate){

		var CartView = BaseView.extend({
			el: "div#cart",
			template: _.template(cartTemplate),
			initialize: function(options){
				options || (options = {});
				this.cart = options.cart || new CartModel({}, {'vent': this.vent});
				this.bindTo(this.cart, 'change', this.render);
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				var data = this.cart.toJSON();
				this.$el.append(this.template(data));

				// Categories in cart
				_.each(data['content'], function(category, i){
					var view = new CategoryInCartView({'content': category, 'vent': this.vent});
					var products = new MiniProductsCollection( category.products, {'vent': this.vent});
					var productsView = new MiniProductsView({'products': products, 'vent': this.vent});
					this.addSubView(view);
					this.addSubView(productsView);
				}, this);

				// Rendering sub views
				_.each(this.subViews, function(view, i){
					this.$el.find('div#cart-recap-accordion').append(view.render().el);
				}, this)
				return this;
			} 
		});


		return CartView;

})