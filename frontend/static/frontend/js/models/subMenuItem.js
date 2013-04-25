define([
	'models/base'
	], function(BaseModel){
		var SubMenuItem = BaseModel.extend({
			defaults:{
				'name': 'Test',
				'parent_brand': null,
				'url': ''
			},
			initialize: function(){
			}
		});
		return SubMenuItem;
})