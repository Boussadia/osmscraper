define([
	'jquery',
	'underscore',
	'backbone',
], function($, _, Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'categorie/:categoryName': 'category',
			'*any':'any'
		},
		initialize: function(options){
			options || (options = {})
			this.vent = options.vent || null;
		},
		category: function(categoryName){
			this.vent.trigger('route:category', {'name': categoryName});
		},
		any: function(any){
		}
	});

	return Router;
});