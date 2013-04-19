define([
	'backbone',
	'models/base',
	'collections/subMenu'
	], function(Backbone, BaseModel, SubMenuCollection){
		var MenuItem = BaseModel.extend({
			default:{
				'name': 'Test',
				'url': ''
			},
			initialize: function(){
				this.subMenu = new SubMenuCollection(this.attributes.subs);
			}
		});
		return MenuItem;
})