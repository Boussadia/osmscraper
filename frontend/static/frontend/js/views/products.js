define([
	'underscore',
	'modernizr',
	'collections/products',
	'views/base',
	'views/product',
	'text!../../templates/products.html',
	'text!../../templates/plus.html'
	],
	function(_, Modernizr, ProductsCollection, BaseView, ProductView, productsTemplate, plusTemplate){

		var ProductsView = BaseView.extend({
			// This variable controlls whether or not to fetch products from server when requested
			fetching: false, 

			// Products width
			PRODUCT_WIDTH: 175,
			rendered: false,

			tagName:'div',
			className: 'products',
			template: _.template(productsTemplate),

			initialize: function(options){
				options || (options = {});
				this.products = options.products || new ProductsCollection([], {'vent': this.vent});
				var that = this;
				this.bindTo(this.products, 'request', function(){
					that.fetching = true;
				});

				this.bindTo(this.products, 'sync', function(){
					// that.render()
					this.fetching = false;
				});

				this.bindTo(this.products, 'add', this.render);
			},
			render: function(product){
				if(typeof product !== 'undefined'){
					var view = new ProductView({'product': product, 'vent': this.vent})
					this.addSubView(view);
					this.$el.append(view.render().el);
				}else{
					this.closeSubViews();
					this.$el.empty();
					var that = this;
					this.products.each(function(product){
						var view = new ProductView({'product': product, 'vent': this.vent})
						that.$el.append(view.render().el);
					});
				}

				// Adding plus button if more products are available to fetch
				if(!Modernizr.touch){
					var plus;
					if (this.$el.find('.add-box').length === 0){
						plus = _.template(plusTemplate)();
					}else{
						plus = this.$el.find('.add-box').parent().remove();
						// console.log(plus)
					}

					if (this.products.length < this.products.count) this.$el.append(plus);
					var outerWidth = this.$el.find('.product').outerWidth();
					if(outerWidth){
						// Setting width
						this.$el.find('.product').width(outerWidth+'px')
						var products_count = this.$el.find('.product').length;
						this.$el.width(outerWidth*products_count*1.1);
					}
				};

				if(Modernizr.touch){
					this.$el.parent().addClass('touch');
					if (this.products.length>5) this.$el.width(this.products.length*this.PRODUCT_WIDTH);
				}


				this.$el.parent().bind( 'scroll', {context: this}, this.touchSwipeListener);

				
				return this;
			},
			events: {
				'click div.add-box': 'getMoreProducts',
			},
			touchSwipeListener: function(e){
				e.preventDefault();

				
				try{
					var that = e.data.context;
					// var that = this;
					var $el = that.$el;
					var base_width = $el.parent().outerWidth();
					var width = $el.outerWidth();
					var left = $el.find('.product').offset().left;
					var calculus = (left+width-base_width)/base_width;
					if(calculus<.2){
						that.getMoreProducts(e);

					}
				}catch(err){
					console.log(err);
				}
			},
			getMoreProducts: function(e){
				var vent = this.vent;
				if (!this.fetching){
					this.products.fetch({
						more: true,
						'vent': vent,
					});
				}
			}
		})

		return ProductsView;
})