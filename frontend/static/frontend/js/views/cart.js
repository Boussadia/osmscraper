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
				// Representing current_cart, if current cart changed, fetched current cart from server
				this.cart = options.cart || new CartModel({}, {'vent': this.vent});
				this.suggested_cart = options.suggested_cart || new CartModel({}, {'vent': this.vent});
				this.osms = options.osms;

				this.vent.on('osm', function(osm){
					if(this.cart.get('name') !== osm.name){
						this.cart.fetch();
					}
				}, this);

				this.vent.on('show:panier', this.show, this);
				this.vent.on('hide:panier', this.hide, this);

				// Rendering when cart changes
				this.bindTo(this.cart, 'change', this.render);

			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				// Getting data for current cart
				var data = {};
				data['current'] = this.cart.toJSON();
				this.$el.append(this.template(data));
			

				// Categories in cart
				_.each(data['current']['content'], function(category, i){
					var view = new CategoryInCartView({'el': this.$el.find('#current_cart .accordion-header'), 'content': category, 'vent': this.vent});
					var products = new MiniProductsCollection( category.products, {'vent': this.vent});
					var productsView = new MiniProductsView({'products': products, el:this.$el.find('#current_cart .products-recap'), 'vent': this.vent});
					this.addSubView(view);
					this.addSubView(productsView);
				}, this);

				// Rendering sub views
				_.each(this.subViews, function(view, i){
					this.$el.find('div#cart-recap-accordion').append(view.render().el);
				}, this)

				// $('#cart-recap-accordion').accordion();
				return this;
			},
			show: function(){
				$('.block-right').addClass('open-cart')
			},
			hide: function(){
				$('.block-right').removeClass('open-cart')
			},
			set_fixed_position: function(){
				var scrollTop = $(window).scrollTop();
				var parent = this.$el;
				parent.removeClass('transition');
				if(scrollTop>this.TRIGGER){
					parent.addClass('top');
				}else if(scrollTop<=this.TRIGGER){
					parent.removeClass('top');
				}
				setTimeout(function(){parent.addClass('transition');}, 100);
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