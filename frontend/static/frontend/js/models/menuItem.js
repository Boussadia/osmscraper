define([
	'backbone',
	'collections/subMenu'
	], function(Backbone, SubMenuCollection){
		var MenuItem = Backbone.Model.extend({
			default:{
				'name': 'Test',
				'url': ''
			},
			initialize: function(attributes, option){
				this.vent = option.vent || {};
				var subs = this.attributes.subs;
				if (subs !== undefined){
					this.subMenu =new SubMenuCollection(subs, {'vent': this.vent});
				}else{
					this.subMenu = {};
				}
			}
		});
		return MenuItem;
})