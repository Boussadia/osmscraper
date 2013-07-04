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
				this.substitutionView = new SubstitutionView({el: $('#substitution'), 'osms': this.osms, 'vent':this.vent});
				this.vent.on('product:recomandation', this.substitution, this);

			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				// Getting data for current cart
				var data = {};
				data = this.cart.toJSON();
				data['suggested'] = this.cart.suggested;
				data['osms'] = this.osms.toJSON()
				data['price_to_save'] = this.osms.get_price_to_save()
				this.$el.append(this.template(data));
			

				// Categories in cart
				_.each(data['content'], function(category, i){
					var view = new CategoryInCartView({'content': category, 'suggested':this.cart.suggested, 'vent': this.vent});
					this.addSubView(view);
					this.$el.find('.scrollarea').append(view.render().el);
				}, this);

				// Controlling loader on osm switch request
				var that = this;
				this.bindTo(this.osms, 'request', function(model, resp, xhr){
					that.showLoader();
				});

				this.bindTo(this.osms, 'sync', function(model, resp, xhr){
					that.hideLoader();
				});
				
	
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
				'click p.empty': 'empty',
				'click .osm-recap .cta': 'switchOSM',
				'click .cta.commander': 'showExport',
			},
			cartClickHandler: function(e){
				this.$el.hasClass('open') ? this.$el.removeClass('open') : this.$el.addClass('open');
			},
			substitution: function(product){
				var that = this;
				var osm_name = product.get('osm_suggested_from');
				var reference = product.toJSON()[osm_name+'_product'].reference;

				product.fetch({
					'data':{
						'osm_name': osm_name,
					},
					'reference': reference,
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
			},
			switchOSM: function(e){
				var $cta = $(e.target);
				var osm = $cta.attr('data-osm');
				if (osm) this.vent.trigger('osm:require:switch', {'name': osm});
			},
			showExport: function(e){
				this.vent.trigger('modal:show:export');
			},
			showLoader: function(){
				this.$el.find('.loader').show();
				this.$el.find('#osms-area .cta').hide();
			},
			hideLoader: function(){
				this.$el.find('.loader').hide();
				this.$el.find('#osms-area .cta').show();
				
			}

		});


		return CartView;

})