define([
	'collections/base',
	'models/menuItem'
	],function(BaseCollection, MenuItem){

		var Menu = BaseCollection.extend({
			model: MenuItem,
			url: '/api/categories/all'
		});

		return Menu;
})