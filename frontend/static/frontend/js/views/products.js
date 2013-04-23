define([
	'underscore',
	'collections/products',
	'views/base',
	'views/product',
	'text!../../templates/products.html'
	],
	function(_, ProductsCollection, BaseView, ProductView, productsTemplate){

		var ProductsView = BaseView.extend({
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
				var data = {'name': this.products.name, 'products': this.products.toJSON()};
				this.$el.append(template(data));
				// var that = this;
				// this.products.each(function(product){
				// 	var view = new ProductView({'product': product, 'vent': this.vent});
				// 	that.addSubView(view);
				// })
				// _.each(this.subViews, function(subView){
				// 	that.$el.append(subView.render().$el);
				// })
				return this;
			}
		})

		return ProductsView;
})