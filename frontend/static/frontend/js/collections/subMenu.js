define([
	'jquery',
	'underscore',
	'backbone',
	'collections/base',
	'models/subMenuItem'
	],function($, _, Backbone, BaseCollection, SubMenuItem){

		var SubMenu = BaseCollection.extend({
			model: SubMenuItem,
			initialize: function(){
			}
		});

		return SubMenu;
})