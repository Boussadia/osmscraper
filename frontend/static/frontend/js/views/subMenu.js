define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'views/subMenuItem',
	'collections/subMenu'
	], function($, _, Backbone, BaseView, SubMenuItemView, SubMenuCollection){

		var SubMenuView = BaseView.extend({
			initialize: function(option){
				this.vent = option.vent || null;
				var models = option.models || {};
				this.subMenuCollection = new SubMenuCollection({}, {'vent': this.vent, 'models': models});
				this.bindTo(this.subMenuCollection, 'reset', function(a, b){
					this.render();
				}, this);

				// Get menu elements from server
				// this.menuCollection.fetch();
			},
			render: function(){
				this.$el.empty();
				this.menuCollection.each(function(menuitem){
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