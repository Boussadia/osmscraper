define([
	'jquery',
	'underscore',
	'backbone',
], function($, _, Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'*any':'any'
		},
		any: function(any){
		}
	});

	return Router;
});