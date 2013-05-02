define([
	'collections/base',
	'models/category'
	],function(BaseCollection, CategoryModel){
		
		var CategoryCollection = BaseCollection.extend({
			// Argument that tells if this is the current category that is displayed in main
			current: false,

			model: CategoryModel,
			url: function(){
				return '/api/categories/id/'+this.id+'/subs';
			},
			initialize: function(models, options){
				options || (options = {});
				this.id = options.id || null;
			},
			parse: function(resp, xhr){
				var that = this;
				// Adding promotion category
				resp.category.subs.unshift({
					id: that.id,
					leave: true,
					name: "promotions",
					parent_category: that.id,
					position: 0,
				})
				return resp.category.subs;
			}

		});

		return CategoryCollection;
})