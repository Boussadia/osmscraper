define([
	'underscore',
	'collections/category',
	'views/base',
	'views/products',
	'text!../../templates/category.html'
	],
	function(_, CategoryCollection, BaseView, ProductsView, categoryTemplate){

		var CategoryCollectionView = BaseView.extend({
			className: 'category',
			template: _.template(categoryTemplate),
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
					if(category.get('count') !== 0){
						var products = category.products;
						var data = category.toJSON();
						var rendered = that.template(data);
						that.$el.append(rendered);
						var view = new ProductsView({'products': products,'el': that.$el.find('.products-container'), 'vent': that.vent});
						that.addSubView(view);
					}
				})

				// Separation between title and products
				_.each(this.subViews, function(subView){
					subView.render().el;
				})
				return this;
			},
			showOrHide: function(options){
				options || (options = {});
				var category_id = options.id || 0;

				if (category_id && this.collection.id === category_id && this.collection.current_osm === this.collection.osm){
					this.collection.current = true;
					this.$el.show();
				}else if(category_id && (this.collection.id !== category_id || this.collection.current_osm !== this.collection.osm)){
					this.collection.current = false;
					this.$el.hide();
				}
			}
		});



		return CategoryCollectionView;

})