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

				// Global Events binding
				// this.vent.on('category:next:sub', this.next_sub_category, this);
			},
			parse: function(resp, xhr){
				// this.attributes = resp.category;
				return resp.category.subs;
			},
			next_sub_category: function(obj){
				obj || (obj = {});
				var category_id = obj.id || null;

				if (category_id && category_id == this.id){
					console.log('c\'est moi ! ');
				}
			}

		});

		return CategoryCollection;
})