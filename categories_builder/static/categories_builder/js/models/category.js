define([
	'backbone'
	], function(Backbone){
		var Category = Backbone.Model.extend({
			default:{
				'name': 'category',
				'parent_category': null,
				'position': 0,
				'url': null,
			},
			initialize: function(){

			}
		});
		return Category;

})