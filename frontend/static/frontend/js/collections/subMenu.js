define([
	'collections/base',
	'models/subMenuItem'
	],function(BaseCollection, SubMenuItem){

		var SubMenu = BaseCollection.extend({
			model: SubMenuItem,
			initialize: function(){
			}
		});

		return SubMenu;
})