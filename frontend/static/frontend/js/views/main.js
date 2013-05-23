define([
	'underscore',
	'views/base',
	'models/category',
	'collections/category',
	'views/categoryCollection'
], function(_, BaseView, CategoryModel, CategoryCollection, CategoryCollectionView){

	var MainView = BaseView.extend({
		el: 'section#main div.block-left',
		SCROLL_TRIGGER: 90,
		initialize: function(options){
			this.current_osm = options.current_osm;
			this.categories = {};
			this.categories[this.current_osm] = [];

			// Global event listening
			this.vent.on('window:scroll', this.scrollController, this);

			// Updating current osm
			this.vent.on('osm', function(osm){
				this.current_osm = osm.name;
				if (!this.categories[this.current_osm]) this.categories[this.current_osm] = [];
				this.vent.trigger('route:category:force');
			}, this);
		},
		addCategory: function(category_id){
			// First we have to determine if the category was already fetched from server or not.
			var category_already_fetched = false;
			var index = null
			var index_insert = 0;

			var categories = this.categories[this.current_osm];

			_.each(categories, function(category, i){
				if(category.id == category_id){
					category_already_fetched = true;
					category.current = true;
					index = i;
				}else if(category.id < category_id){
					index_insert = i + 1;
					category.current = false;
				}
			}, this)

			if (!category_already_fetched){
				// If the category was not fetched, proceed
				var categoryCollection = new CategoryCollection([], {'id': category_id,'osm': this.current_osm, 'vent': this.vent});
				categoryCollection.current = true;
				categories.splice(index_insert, 0, categoryCollection);

				var that = this;
				var that = this;
				categoryCollection.fetch({
					success:function(collection, response, options){
						collection.each(function(model){
							model.vent = that.vent;
							model.fetch_products({
								'success': function(coll, resp, opt){
									coll.each(function(mod){
										mod.vent = that.vent;
									})
								}
							});
						});
						that.render(categoryCollection)
					}
				});
			}
		},
		render: function(categoryCollection){
			var view = new CategoryCollectionView({'collection': categoryCollection, 'vent': this.vent});
			this.addSubView(view);
			this.$el.append(view.render().el);
			categoryCollection.current ? view.$el.show() : view.$el.hide();
			return this;

		}
	});


	return MainView;
})