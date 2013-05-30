define([
	'underscore',
	'models/cart',
	'views/base',
	'views/category-in-cart',
	'text!../../templates/cart.html',
	'jqueryUi'
	], function(_, CartModel, BaseView, CategoryInCartView, cartTemplate){

		var CartView = BaseView.extend({
			el: "div#cart",
			template: _.template(cartTemplate),
			TRIGGER: 138,
			initialize: function(options){
				options || (options = {});
				// Representing current_cart, if current cart changed, fetched current cart from server
				this.cart = options.cart || new CartModel({}, {'vent': this.vent});
				this.osms = options.osms;

				this.vent.on('show:panier', this.show, this);
				this.vent.on('hide:panier', this.hide, this);

				// Rendering when cart changes
				this.bindTo(this.cart, 'change', this.render);

			},
			render: function(){
				if(this.cart.get('name') !== this.cart.suggested){
					this.closeSubViews();
					this.$el.empty();
					// Getting data for current cart
					var data = {};
					data = this.cart.toJSON();
					data['suggested'] = this.cart.suggested;
					this.$el.append(this.template(data));
				

					// Categories in cart
					_.each(data['content'], function(category, i){
						var view = new CategoryInCartView({'content': category, 'suggested':this.cart.suggested, 'vent': this.vent});
						this.addSubView(view);
						this.$el.find('.scrollarea').append(view.render().el);
					}, this);

					// $('#cart-recap-accordion').accordion();
				}
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