define([
	'underscore',
	'views/base',
	'collections/category',
	'views/categoryCollection'
], function(_, BaseView, CategoryCollection, CategoryCollectionView){

	var MainView = BaseView.extend({
		el: 'section#main',
		initialize: function(){
			this.categories = [];
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

		}
	});


	return MainView;
})