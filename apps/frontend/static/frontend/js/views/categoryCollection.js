define([
	'underscore',
	'jquery',
	'collections/category',
	'views/base',
	'views/products',
	'text!../../templates/category.html'
	],
	function(_, $, CategoryCollection, BaseView, ProductsView, categoryTemplate){

		var CategoryCollectionView = BaseView.extend({
			className: 'category',
			template: _.template(categoryTemplate),
			initialize: function(options){
				options || (options = {});
				this.collection = options.collection || new CategoryCollection([], {'vent': this.vent});
				this.osms = options.osms;

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
						products.count = category.get('count');
						data['threshold'] = products.PRODUCTS_PER_PAGE;
						var rendered = that.template(data);
						that.$el.append(rendered);
						var view = new ProductsView({'products': products,'el': that.$el.find('.products:last-child .products-container'), 'vent': that.vent});
						that.bindTo(products, 'sync', function(model, resp, options){
							that.controllerDisplay(model);
						});
						that.addSubView(view);
					}
				})

				// Separation between title and products
				_.each(this.subViews, function(subView){
					subView.render().el;
				})
				return this;
			},
			events: {
				'click .controller.right': 'moreProducts',
				'click .controller.left': 'lessProducts',
			},
			moreProducts: function(e){
				var id_category = parseInt($(e.target).attr('data-id'));
				var view = _.find(this.subViews, function(view, i){
					return view.products.id === id_category;
				}, this);
				if (view){
					var that = this;
					view.more(function(){
						that.controllerDisplay(view.products)
					})
				};
			},
			lessProducts: function(e){
				var id_category = parseInt($(e.target).attr('data-id'));
				var view = _.find(this.subViews, function(view, i){
					return view.products.id === id_category;
				}, this);
				if (view){
					var that = this;
					view.less(function(){
						that.controllerDisplay(view.products)
					})
				};
			},
			showOrHide: function(options){
				options || (options = {});
				var category_id = options.id || 0;
				var current_osm = this.osms.get_active_osm();

				if (category_id && this.collection.id === category_id && current_osm.get('name') === this.collection.osm){
					this.collection.current = true;
					this.$el.show();
				}else if(category_id && (this.collection.id !== category_id || current_osm.get('name') !== this.collection.osm)){
					this.collection.current = false;
					this.$el.hide();
				}
			},
			controllerDisplay: function(products){
				var products_id = products.id;
				var page = products.page;
				var max_pages = products.max_pages;
				
				if(max_pages <= page){
					this.$el.find('.controller.right[data-id='+products_id+']').hide();
				}else{
					this.$el.find('.controller.right[data-id='+products_id+']').show();
				}
				if(page<=1){
					this.$el.find('.controller.left[data-id='+products_id+']').hide();
				}else{
					this.$el.find('.controller.left[data-id='+products_id+']').show();
				}
			}
		});



		return CategoryCollectionView;

})