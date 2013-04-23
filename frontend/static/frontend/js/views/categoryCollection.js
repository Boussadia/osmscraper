define([
	'underscore',
	'collections/category',
	'views/base',
	'views/products'
	],
	function(_, CategoryCollection, BaseView, ProductsView){

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
				_.each(this.subViews, function(subView){
					that.$el.append(subView.render().$el);
				})
				return this;
			}
		});



		return CategoryCollectionView;

})