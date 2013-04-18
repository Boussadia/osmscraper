define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'views/menuitem',
	'collections/menu'
	], function($, _, Backbone, BaseView, MenuItemView, MenuCollection){

		var MenuView = BaseView.extend({
			el: 'nav#menu ul.left',
			initialize: function(options){
				options || (options = {});
				this.models = options.model || {};
				this.menuCollection = new MenuCollection(this.models, {'vent': this.vent});
				this.bindTo(this.menuCollection, 'add remove', function(a, b){
					this.render();
				}, this);

				// Get menu elements from server
				this.menuCollection.fetch();
			},
			render: function(){
				this.$el.empty();
				this.menuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this)
				return this;
			},
			addOne: function(menuItem){
				var divider = $('<li>').attr('class', 'divider');
				var view = new MenuItemView({'model':menuItem});
				this.$el.append(view.render().el);
				this.$el.append(divider);
			}
		});

		return MenuView;
})