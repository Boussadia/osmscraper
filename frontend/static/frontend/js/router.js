define([
	'jquery',
	'underscore',
	'backbone',
], function($, _, Backbone){
	Router = Backbone.Router.extend({
		routes: {
			'*any':'any'
		},
		initialize: function(option){
			this.vent = option.vent || null;
		},
		any: function(any){
		}
	});

	return Router;
});