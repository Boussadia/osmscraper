define([
	'underscore',
	'views/base',
	'views/menuitem',
	'views/saveAndOrder',
	'views/subMenu',
	'collections/menu'
	], function(_, BaseView, MenuItemView, SaveAndOrderView, SubMenuView, MenuCollection){

		var MenuView = BaseView.extend({
			el: 'nav#menu ul.left',
			TRIGGER: 138,
			initialize: function(options){
				options || (options = {});
				this.models = options.model || {};
				this.menuCollection = new MenuCollection(this.models, {'vent': this.vent});

				this.saveAndOrderView = new SaveAndOrderView({'vent': this.vent});

				// Global events binding
				this.vent.on('menu:closeSubViews', this.hideSubViews, this);
				this.vent.on('route:category', this.send_category_id, this);
				this.vent.on('window:scroll', this.set_menu_position, this);
			},
			render: function(callback){
				this.closeSubViews();
				this.$el.empty();
				this.menuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this);

				// Adding ECONOMISER and COMMANDER
				this.addSubView(this.saveAndOrderView);
				this.$el.append(this.saveAndOrderView.render().el);
				this.addSubView(this.saveAndOrderView.orderView);
				this.$el.append(this.saveAndOrderView.orderView.render().el);

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
					success:function(){
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
				var categoryURL = options.url || '';
				var result = null;
				this.menuCollection.each(function(menuItem, i){
					var lookup = menuItem.subMenu.findWhere({'url': categoryURL});
					if (lookup){
						var category_id = lookup.get('id');
						this.subViews[i].showSubMenu(); // Highlighting main menu
						this.vent.trigger('route:category', {'id': category_id});
					};
				}, this)
			},
			set_menu_position: function(){
				var scrollTop = $(window).scrollTop();
				var parent = $('header');
				if(scrollTop>this.TRIGGER){
					parent.addClass('top');
					// parent.css('top',(scrollTop-7)+'px');
				}else if(scrollTop<=this.TRIGGER){
					parent.removeClass('top');
					// parent.css('top', '0px');
				}
			}
		});

		return MenuView;
})