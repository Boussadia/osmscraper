define([
	'backbone'
	], function(Backbone){
		var MenuItem = Backbone.Model.extend({
			default:{
				'name': 'Test',
				'parent_brand': null,
				'url': ''
			},
			initialize: function(){
			}
		});
		return MenuItem;
})