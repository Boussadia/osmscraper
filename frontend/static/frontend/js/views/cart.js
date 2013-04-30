define([
	'underscore',
	'collections/miniproducts',
	'models/cart',
	'views/base',
	'views/category-in-cart',
	'views/mini-products',
	'text!../../templates/cart.html',
	'jqueryUi'
	], function(_, MiniProductsCollection, CartModel, BaseView, CategoryInCartView, MiniProductsView, cartTemplate){

		var CartView = BaseView.extend({
			el: "div#cart",
			template: _.template(cartTemplate),
			TRIGGER: 138,
			initialize: function(options){
				options || (options = {});
				this.cart = options.cart || new CartModel({}, {'vent': this.vent});
				this.bindTo(this.cart, 'change', this.render);
				this.vent.on('window:scroll', this.set_fixed_position, this);
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

				$('#cart-recap-accordion').accordion();
				return this;
			},
			set_fixed_position: function(){
				var scrollTop = $(window).scrollTop();
				var parent = this.$el;
				if(scrollTop>this.TRIGGER){
					parent.addClass('top');
					// parent.css('top',(scrollTop-7)+'px');
				}else if(scrollTop<=this.TRIGGER){
					parent.removeClass('top');
					// parent.css('top', '0px');
				}
			},
			events: {
				'click div#cart-icone': 'cartClickHandler',
			},
			cartClickHandler: function(e){

				this.$el.hasClass('open') ? this.$el.removeClass('open') : this.$el.addClass('open');
			}
		});


		return CartView;

})