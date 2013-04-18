define([
	'backbone',
	'models/base'
	], function(Backbone, BaseModel){
		var SubMenuItem = BaseModel.extend({
			default:{
				'name': 'Test',
				'parent_brand': null,
				'url': ''
			},
			initialize: function(){
			}
		});
		return SubMenuItem;
})