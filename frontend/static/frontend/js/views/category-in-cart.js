define([
	'underscore',
	'collections/miniproducts',
	'views/base',
	'views/mini-products',
	'text!../../templates/category-in-cart.html'
	], function(_, MiniProductsCollection, BaseView, MiniProductsView, categoryInCartTemplate){

		var CategoryInCartView = BaseView.extend({
			template: _.template(categoryInCartTemplate),
			className:'cart-recap-accordion',
			initialize: function(options){
				options || (options = {});
				this.data = options.content;
				this.suggested = options.suggested;

			},
			render: function(){
				this.$el.empty();
				var data = this.data;
				data['suggested'] = this.suggested;
				this.$el.append(this.template(data));

				// Products in category
				var products = new MiniProductsCollection( data.products, {'vent': this.vent,'suggested': this.suggested});
				var productsView = new MiniProductsView({'products': products, el:this.$el.find('.products-recap'), 'vent': this.vent});
				this.addSubView(productsView);
				productsView.render();
				
				return this;
			}
		});

		return CategoryInCartView;
});