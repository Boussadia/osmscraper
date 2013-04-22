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
			var categoryCollection = new CategoryCollection({'id': category_id, 'vent': this.vent});
			this.categories.push(categoryCollection);
			var view = new CategoryCollectionView({'collection': categoryCollection, 'vent': this.vent});
			this.addSubView(view);
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
		},
		render: function(){
			var that = this;
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

			}
		}
	});


	return MainView;
})