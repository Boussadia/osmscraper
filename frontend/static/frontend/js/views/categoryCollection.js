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

				// Global events
				this.vent.on('route:category', this.showOrHide, this);
			},
			render: function(){
				this.closeSubViews();
				var that = this;
				this.collection.each(function(category){
					var products = category.products;
					var view = new ProductsView({'products': products, 'vent': that.vent});
					that.addSubView(view);
				})
				// Separation between title and products
				_.each(this.subViews, function(subView){
					that.$el.append(subView.render().$el);
				})
				return this;
			},
			showOrHide: function(options){
				options || (options = {});
				var category_id = options.id || 0;

				if (category_id && this.collection.id === category_id){
					this.collection.current = true;
					this.$el.show();
				}else if(category_id && this.collection.id !== category_id){
					this.collection.current = false;
					this.$el.hide();
				}
			}
		});



		return CategoryCollectionView;

})