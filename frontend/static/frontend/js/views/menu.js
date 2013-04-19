define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'views/menuitem',
	'views/subMenu',
	'collections/menu'
	], function($, _, Backbone, BaseView, MenuItemView, SubMenuView, MenuCollection){

		var MenuView = BaseView.extend({
			el: 'nav#menu ul.left',
			initialize: function(options){
				options || (options = {});
				this.models = options.model || {};
				this.menuCollection = new MenuCollection(this.models, {'vent': this.vent});

				// Get menu elements from server
				var that = this;
				this.menuCollection.fetch({
					'success':function(){
						that.render();
						that.bindTo(that.menuCollection, 'add remove', function(a, b){
							this.render();
						}, that);
					}
				});

				this.vent.on('menu:closeSubViews', this.hideSubViews, this)
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				this.menuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this)
				return this;
			},
			addOne: function(menuItem){
				var divider = $('<li>').attr('class', 'divider');
				var view = new MenuItemView({'model':menuItem, 'vent': this.vent});
				this.addSubView(view);
				this.$el.append(view.render().el);
				this.$el.append(divider);

				// console.log(menuItem.attributes.subs);

				var subMenuView = new SubMenuView({'models': menuItem.attributes.subs, 'vent': this.vent});
				view.addSubView(subMenuView);
				view.$el.find('.submenu').append(subMenuView.render().el);
			},

			hideSubViews: function(e){
				_.each(this.subViews, function(view){
					view.hideSubMenu();
				}, this)
			}
		});

		return MenuView;
})