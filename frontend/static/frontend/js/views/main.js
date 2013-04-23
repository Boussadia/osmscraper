define([
	'underscore',
	'views/base',
	'collections/category',
	'views/categoryCollection'
], function(_, BaseView, CategoryCollection, CategoryCollectionView){

	var MainView = BaseView.extend({
		el: 'section#main',
		SCROLL_TRIGGER: 90,
		initialize: function(){
			this.categories = [];

			// Global event listening
			this.vent.on('window:scroll', this.scrollController, this);
		},
		addCategory: function(category_id){
			// First we have to determine if the category was already fetched from server or not.
			var category_already_fetched = false;
			var index = null
			var index_insert = 0;
			_.any(this.categories, function(category, i){
				if(category.id == category_id){
					category_already_fetched = true;
					index = i;
					return true
				}else if(category.id < category_id){
					index_insert = i + 1;
				}
			})

			if (!category_already_fetched){
				// If the category was not fetched, proceed
				var categoryCollection = new CategoryCollection([], {'id': category_id, 'vent': this.vent});
				this.categories.splice(index_insert, 0, categoryCollection);
				var view = new CategoryCollectionView({'collection': categoryCollection, 'vent': this.vent});
				this.addSubView(view, index_insert);
				var that = this;
				this.bindTo(categoryCollection, 'add', function(){
					that.render();
				});
				var that = this;
				categoryCollection.fetch({
					'success':function(collection, response, options){
						collection.each(function(model){
							model.fetch_products();
						});
					}
				});
			}else{
				// The category is already here, show it at the top of the screen
				var top = this.subViews[index].$el.offset().top;
				$(window).scrollTop(top, 0);

			}
		},
		render: function(){
			var that = this;
			that.$el.empty();
			_.each(this.subViews, function(view){
				that.$el.append(view.render().el);
			});
			return this;

		},
		scrollController: function(){
			var offset = this.$el.offset(),
				scrollTop = $(window).scrollTop(),
				bottom_main = offset.top + this.$el.height(),
				visibleHeight = 0;
			if (window.innerHeight){
				visibleHeight = window.innerHeight;
			}else{
				visibleHeight = window.clientHeight;
			}

			var difference = bottom_main - (scrollTop + visibleHeight);

			if (difference < this.SCROLL_TRIGGER){
				// TODO : here put code to call for next categorie to fetch
				var l = this.categories.length;
				var last_category = this.categories[l-1];
				this.vent.trigger('category:next:sub', {'id': last_category.id});
			}
		}
	});


	return MainView;
})