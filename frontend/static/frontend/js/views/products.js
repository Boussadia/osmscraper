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
			tagName:'div',
			className: 'products',
			template: _.template(productsTemplate),
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
				var data = {'name': this.products.name, 'count': this.products.count};
				this.$el.append(this.template(data));
				var that = this;
				this.products.each(function(product){
					var view = new ProductView({'product': product, 'vent': this.vent})
					that.$el.append(view.render().el);
				})

				var plus = _.template(plusTemplate)();
				this.$el.append(plus);

				return this;
			}
		})

		return ProductsView;
})