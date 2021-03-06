define([
	'underscore',
	'jquery',
	'collections/category',
	'views/base',
	'views/products',
	'views/brands-filter',
	'views/price-filter',
	'text!../../templates/category.html'
	],
	function(_, $, CategoryCollection, BaseView, ProductsView, BrandsFilterView, PriceFilterView, categoryTemplate){

		var CategoryCollectionView = BaseView.extend({
			className: 'category',
			template: _.template(categoryTemplate),
			initialize: function(options){
				options || (options = {});
				this.collection = options.collection || new CategoryCollection([], {'vent': this.vent});
				this.osms = options.osms;

				// Global events
				this.vent.on('route:category', this.showOrHide, this);
				this.vent.on('brands:filter', this.updateView, this);
				this.vent.on('brands:filter price:filter', this.filter, this);
			},
			render: function(){
				this.closeSubViews();
				var that = this;
				this.collection.each(function(category){
					if(category.get('count') !== 0){
						// Rendering brands filter
						var data = category.toJSON();

						// Rendering products
						var products = category.products;
						data['threshold'] = products.PRODUCTS_PER_PAGE;
						var rendered = that.template(data);
						that.$el.append(rendered);

						var view = new ProductsView({'products': products,'el': that.$el.find('.products:last-child .products-container'), 'vent': that.vent});
						that.bindTo(products, 'sync', function(model, resp, options){
							that.controllerDisplay(model);
						});
						
						products.once('sync', function(){
							// Pre Fetching products here (its a hack :/)
							view.$el.removeClass('transition-l'); 
							products.once('sync', function(){
								var products_id = view.products.id;
								var left_controller = that.$el.find('.controller.left[data-id='+products_id+']');
								left_controller.click();
								view.$el.addClass('transition-l'); 
							})
							view.more();
						});

						that.bindTo(view, 'fetching', function(options){
							var category_id = view.products.id;
							var display = !options.fetched;
							if (display) this.$el.find('.products[data-id='+category_id+'] .loader').show();
							if (!display) this.$el.find('.products[data-id='+category_id+'] .loader').hide();
						});
						that.addSubView(view);

						var data_brands = data.brands.content;
						var filter_view = new BrandsFilterView({'brands': data_brands, 'category_id': products.id, 'el': that.$el.find('.products:last-child ul.brands'), 'vent': that.vent});
						that.addSubView(filter_view);

						var data_price_filter = [{
							'id': 0,
							'name': 'Pas de filtre',
							'checked': true
						},{
							'id': 1,
							'name': 'Filtre par prix',
							'checked': false
						},{
							'id': 2,
							'name': ' Filtre par prix au Kg ou L',
							'checked': false
						}]

						var price_filter_view = price_filter_view = new PriceFilterView({'filters': data_price_filter, 'category_id': products.id, 'el': that.$el.find('.products:last-child ul.price-filter'), 'vent': that.vent});
						that.addSubView(price_filter_view);
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
				'click .brands-controller': 'showBrandsFilter',
				'click .price-filter-controller': 'showPriceFilter',
			},
			moreProducts: function(e){
				var id_category = parseInt($(e.target).attr('data-id'));
				var view = _.find(this.subViews, function(view, i){
					if (view.products) return view.products.id === id_category;
					return false
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
					if (view.products) return view.products.id === id_category;
					return false
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
			showBrandsFilter: function(e){
				var hide_handler = function(e){
					var clicked = e.target;
					var is_in = $.contains(view.el, clicked);
					if (!is_in && view.$el.is(":visible")){
						view.$el.css('display', 'none')
						$(window).unbind('click', hide_handler);
					}else{
						view.$el.css('display', 'inline-block');
					}
				}

				// Nasty hack due to extreme laziness 
				setTimeout(function(){
					$(window).bind( 'click', hide_handler);
				}, 500)
				
				var category_id = $(e.target).attr('data-id');
				category_id = parseInt(category_id);
				var view = _.find(this.subViews, function(view, i){
					if (view.category_id && view.$el.attr('class').indexOf('brands')>-1) return view.category_id === category_id;
					return false
				}, this);
				if(view && view.$el.is(":visible")) view.$el.css('display', 'none');
				if(view && !view.$el.is(":visible")) view.$el.css('display', 'inline-block');

			},
			showPriceFilter: function(e){
				var hide_handler = function(e){
					var clicked = e.target;
					var is_in = $.contains(view.el, clicked);
					if (!is_in && view.$el.is(":visible")){
						view.$el.css('display', 'none')
						$(window).unbind('click', hide_handler);
					}else{
						view.$el.css('display', 'inline-block');
					}
				}

				// Nasty hack due to extreme laziness 
				setTimeout(function(){
					$(window).bind( 'click', hide_handler);
				}, 500)
				
				var category_id = $(e.target).attr('data-id');
				category_id = parseInt(category_id);
				var view = _.find(this.subViews, function(view, i){
					if (view.category_id &&  view.$el.attr('class').indexOf('price-filter')>-1) return view.category_id === category_id;
					return false
				}, this);
				if(view && view.$el.is(":visible")) view.$el.css('display', 'none');
				if(view && !view.$el.is(":visible")) view.$el.css('display', 'inline-block');

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
			},
			filter: function(options){
				var category_id = options.id;
				var price_filter_view;
				var brands_filter_view;
				_.each(this.subViews, function(view, i){
					if (view.category_id && view.category_id === category_id && view.selected_brands) brands_filter_view = view;
					if (view.category_id && view.category_id === category_id && (typeof view.selected_filter) ==="number") price_filter_view = view;
				}, this);

				// Getting filter valuess from child views
				var price_filter = price_filter_view.selected_filter;
				var brands_filter = brands_filter_view.selected_brands;

				options = {
					'brands': brands_filter,
					'filter': price_filter,
					'id': category_id
				};

				this.vent.trigger('products:filter', options);
			},
			updateView: function(options){
				var count_brands = options.brands.length;
				var products_id = options.id;
				var max_brands = options.max_count;
				var text_to_show = 'marques : toutes';
				if(count_brands > 0){
					this.$el.find($('.brands-controller[data-id='+products_id+']:nth-child(2)')).text(count_brands);
					if (count_brands > 1) text_to_show = 'marques / '+ max_brands;
					if (count_brands === 1) text_to_show = 'marque / '+ max_brands;
					this.$el.find($('.brands-controller[data-id='+products_id+']:nth-child(3)')).text(text_to_show);
				}else{
					this.$el.find($('.brands-controller[data-id='+products_id+']:nth-child(2)')).text(max_brands);
					this.$el.find($('.brands-controller[data-id='+products_id+']:nth-child(3)')).text(text_to_show);
				}
			}
		});

		return CategoryCollectionView;

})