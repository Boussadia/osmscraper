define([
	'underscore',
	'jquery',
	'collections/products',
	'models/cart',
	'views/base',
	'views/category-in-cart',
	'views/substitution',
	'views/product-in-cart',
	'text!../../templates/cart.html',
	'text!../../templates/product.html',
	'jqueryUi'
	], function(_, $, ProductsCollection, CartModel, BaseView, CategoryInCartView, SubstitutionView, ProductInCartView, cartTemplate, productTemplate){

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

				// Substitution View (apart from other views)
				this.substitutionView = new SubstitutionView({el: $('#substitution'), 'osms': this.osms});
				this.vent.on('product:recomandation', this.substitution, this);

			},
			render: function(){
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


				// Temporary cart rendering
				// var products_array = [];
				// // // Categories in cart
				// _.each(data['content'], function(category, i){
				// 	products_array = products_array.concat(category.products);
				// }, this);

				// products_array = _.uniq(products_array, false, function(element){
				// 	return element.product.reference
				// });

				// var products = new ProductsCollection(products_array, {'vent': this.vent});

				// products.each(function(product){
				// 	this.bindTo(product, 'change', this.render);
				// 	var view = new ProductInCartView({'product': product, 'vent': this.vent});
				// 	this.addSubView(view);
				// 	this.$el.find('.scrollarea').append(view.render().el);
				// }, this);
				
	
				return this;
			},
			show: function(){
				$('#cart-bg').show();
				$('.block-right').addClass('open-cart')
			},
			hide: function(){
				$('#cart-bg').hide();
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
				'click p.empty': 'empty'
			},
			cartClickHandler: function(e){

				this.$el.hasClass('open') ? this.$el.removeClass('open') : this.$el.addClass('open');
			},
			substitution: function(product){
				var that = this;
				var osm_name = product.get('osm_suggested_from');
				product.fetch({
					'data':{
						'osm_name': osm_name,
					},
					'reference': product.toJSON()[osm_name+'_product'].reference,
					success: function(){
						that.substitutionView.product = product;
						that.substitutionView.suggested = that.cart.suggested;
						that.substitutionView.render().$el.show();
					}
				});
			},
			empty: function(e){
				var answer = confirm('Êtes-vous sûr de vouloir vider votre panier ?');

				if (answer) this.cart.empty();
			}

		});


		return CartView;

})