define([
	'jquery',
	'underscore',
	'backbone',
	'models/menuItem'
	],function($, _, Backbone, MenuItem){

		var Menu = Backbone.Collection.extend({
			model: MenuItem,
			url: '/api/categories/all',
			initialize: function(attributes, option){
				this.vent = option.vent || null;
			},
			parse: function(resp, xhr){
				return resp.categories
			}
		});

		return Menu;
})