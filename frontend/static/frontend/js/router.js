define([
	'backbone',
], function(Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'': 'index',
			'categorie/:parentCategoryName/:childCategoryName': 'category',
			'*any':'any'
		},
		initialize: function(options){
			options || (options = {})
			this.vent = options.vent || null;
		},
		index: function(){
			var url = '/categorie/epicerie-sucree/cafes-et-chicorees';
			this.navigate(url, true);
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