define([
	'models/base'
	], function(BaseModel){
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