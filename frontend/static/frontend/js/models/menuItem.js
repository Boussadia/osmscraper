define([
	'models/base',
	'collections/subMenu'
	], function(BaseModel, SubMenuCollection){
		var MenuItem = BaseModel.extend({
			defaults:{
				'name': 'Test',
				'url': ''
			},
			initialize: function(){
				this.subMenu = new SubMenuCollection(this.attributes.subs);

			}
		});
		return MenuItem;
})