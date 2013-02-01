define([
	'backbone'
	], function(Backbone){
		var Brand = Backbone.Model.extend({
			default:{
				'name': 'brand',
				'parent_brand': null,
				'url': ''
			},
			initialize: function(){

			}
		});
		return Brand;

})