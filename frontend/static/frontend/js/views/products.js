define([
	'underscore',
	'collections/products',
	'views/base',
	'views/product',
	'text!../../templates/products.html'
	],
	function(_, ProductsCollection, BaseView, ProductView, productsTemplate){

		var ProductsView = BaseView.extend({
			tagName:'div',
			className: 'products',
			template: productsTemplate,
			initialize: function(options){
				options || (options = {});
				this.products = options.products || new ProductsCollection([], {'vent': this.vent});
				var that = this;
				this.bindTo(this.products, 'add', function(){
					that.render();
				})
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();

				var template = _.template(this.template);
				var data = {'name': this.products.name};
				this.$el.append(template(data));
				var that = this;
				this.products.each(function(product){
					var view = new ProductView({'product': product, 'vent': this.vent})
					that.$el.append(view.render().el);
				})

				return this;
			}
		})

		return ProductsView;
})