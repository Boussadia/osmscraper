define([
	'underscore',
	'collections/products',
	'views/base',
	'views/product',
	'text!../../templates/products.html',
	'text!../../templates/plus.html'
	],
	function(_, ProductsCollection, BaseView, ProductView, productsTemplate, plusTemplate){

		var ProductsView = BaseView.extend({
			// This variable controlls whether or not to fetch products from server when requested
			fetching: false, 

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
				this.bindTo(this.products, 'sync', function(e){
					that.render();
					that.fetching = false;
				});
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				var data = {'name': this.products.name, 'count': this.products.count};
				this.$el.append(this.template(data));
				var that = this;
				this.products.each(function(product){
					var view = new ProductView({'product': product, 'vent': this.vent})
					that.$el.append(view.render().el);
				});


				// Adding plus button if more products are available to fetch
				if(this.products.length < this.products.count){
					var plus = _.template(plusTemplate)();
					this.$el.append(plus);
				};

				return this;
			},
			events: {
				'click div.add-box': 'getMoreProducts'
			},
			getMoreProducts: function(e){
				if (!this.fetching){
					this.products.fetch({
						more: true
					});
				}
			}
		})

		return ProductsView;
})