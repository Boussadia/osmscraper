define([
	'jquery',
	'underscore',
	'backbone',
	'collections/base',
	'models/menuItem'
	],function($, _, Backbone, BaseCollection, MenuItem){

		var Menu = BaseCollection.extend({
			model: MenuItem,
			url: '/api/categories/all',
			initialize: function(){
			},
			parse: function(resp, xhr){
				return resp.categories
			}
		});

		return Menu;
})