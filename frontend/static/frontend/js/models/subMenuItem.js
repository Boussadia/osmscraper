define([
	'backbone'
	], function(Backbone){
		var SubMenuItem = Backbone.Model.extend({
			default:{
				'name': 'Test',
				'parent_brand': null,
				'url': ''
			},
			initialize: function(attributes, option){
			}
		});
		return SubMenuItem;
})