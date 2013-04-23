define([
	'collections/base',
	'models/category'
	],function(BaseCollection, CategoryModel){
		
		var CategoryCollection = BaseCollection.extend({
			model: CategoryModel,
			url: function(){
				return '/api/categories/id/'+this.id+'/subs';
			},
			initialize: function(models, options){
				options || (options = {});
				this.id = options.id || null;
			},
			parse: function(resp, xhr){
				// this.attributes = resp.category;
				return resp.category.subs;
			}

		});

		return CategoryCollection;
})