define([
	'jquery',
	'underscore',
	'backbone',
], function($, _, Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'categorie/:catgoryName': 'category',
			'*any':'any'
		},
		initialize: function(options){
			options || (options = {})
			this.vent = options.vent || null;
		},
		category: function(categoryName){
			this.vent.trigger('route:category', categoryName);
		},
		any: function(any){
		}
	});

	return Router;
});