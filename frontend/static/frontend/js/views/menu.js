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

				this.vent.on('menu:closeSubViews', this.hideSubViews, this);
				this.vent.on('route:category', this.send_category_id, this);
			},
			render: function(callback){
				this.closeSubViews();
				this.$el.empty();
				this.menuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this);
				if (callback) callback();
				return this;
			},
			addOne: function(menuItem){
				var view = new MenuItemView({'model':menuItem, 'vent': this.vent});
				this.addSubView(view);
				this.$el.append(view.render().el);

				var subMenuView = new SubMenuView({'models': menuItem.attributes.subs, 'vent': this.vent});
				view.addSubView(subMenuView);
				view.$el.find('.submenu').append(subMenuView.render().el);
			},
			build: function(callback){
				// Get menu elements from server
				var that = this;
				this.menuCollection.fetch({
					'success':function(){
						that.render(callback);
						that.bindTo(that.menuCollection, 'add remove', function(a, b){
							this.render();
						}, that);
					}
				});
			},
			hideSubViews: function(e){
				_.each(this.subViews, function(view){
					view.hideSubMenu();
				}, this)
			},
			send_category_id: function(options){
				options || (options = {});
				var categoryName = options.name || '';
				var result = null;
				this.menuCollection.each(function(menuItem){
					var lookup = menuItem.subMenu.findWhere({'url': categoryName});
					if (lookup){
						var category_id = lookup.get('id');
						this.vent.trigger('route:category', {'id': category_id});
					};
				}, this)
			}
		});

		return MenuView;
})