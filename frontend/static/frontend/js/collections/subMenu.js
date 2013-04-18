define([
	'jquery',
	'underscore',
	'backbone',
	'models/subMenuItem'
	],function($, _, Backbone, SubMenuItem){

		var SubMenu = Backbone.Collection.extend({
			model: SubMenuItem,
			initialize: function(attributes, option){
				if (option) {
					this.vent = option.vent || null;
				}
				
			}
		});

		return SubMenu;
})