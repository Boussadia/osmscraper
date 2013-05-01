define([
	'backbone',
], function(Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'categorie/:parentCategoryName/:childCategoryName': 'category',
			'*any':'any'
		},
		initialize: function(options){
			options || (options = {})
			this.vent = options.vent || null;
		},
		category: function(parentCategoryName, childCategoryName){
			var url = parentCategoryName+'/'+childCategoryName;
			this.vent.trigger('route:category', {'url': url});
		},
		any: function(any){
		}
	});

	return Router;
});