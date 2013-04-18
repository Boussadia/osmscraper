define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'views/subMenuItem',
	'collections/subMenu'
	], function($, _, Backbone, BaseView, SubMenuItemView, SubMenuCollection){

		var SubMenuView = BaseView.extend({
			initialize: function(options){
				options || (options = {});
				this.models = options.model || {};
				this.subMenuCollection = new SubMenuCollection(this.models, {'vent': this.vent});
				this.bindTo(this.subMenuCollection, 'reset', function(a, b){
					this.render();
				}, this);
			},
			render: function(){
				this.$el.empty();
				this.subMenuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this)
				return this;
			},
			addOne: function(menuItem){
				// var divider = $('<li>').attr('class', 'divider');
				// var view = new MenuItemView({'model':menuItem});
				// this.$el.append(view.render().el);
				// this.$el.append(divider);
			}
		});

		return SubMenuView;
})