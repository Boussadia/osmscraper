define([
	'collections/base',
	'models/category'
	],function(BaseCollection, CategoryModel){
		
		var CategoryCollection = BaseCollection.extend({
			model: CategoryModel,
			url: '/api/categories/id/'+this.id+'/subs',
			initialize: function(options){
				options || (options = {});
				this.id = options.id || null;
			},
			parse: function(resp, xhr){
				return resp.categories
			}

		});

		return CategoryCollection;
})