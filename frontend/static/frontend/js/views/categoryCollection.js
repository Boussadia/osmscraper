define([
	'underscore',
	'collections/category',
	'views/base',
	'views/products',
	'text!../../templates/thin-bar-seperator.html'
	],
	function(_, CategoryCollection, BaseView, ProductsView, seperatorTemplate){

		var CategoryCollectionView = BaseView.extend({
			className: 'category',
			initialize: function(options){
				options || (options = {});
				this.collection = options.collection || new CategoryCollection([], {'vent': this.vent});
			},
			render: function(){
				this.closeSubViews();
				var that = this;
				this.collection.each(function(category){
					var products = category.products;
					var view = new ProductsView({'products': products, 'vent': this.vent});
					that.addSubView(view);
				})
				// Separation between title and products
				_.each(this.subViews, function(subView){
					var separator = _.template(seperatorTemplate);
					that.$el.append(separator({}));
					that.$el.append(subView.render().$el);
				})
				return this;
			}
		});



		return CategoryCollectionView;

})