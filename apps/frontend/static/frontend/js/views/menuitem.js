define([
	'views/base',
	'text!../../templates/menuitem.html'
	],function(BaseView, menuItemTemplate){
		var MenuItemView = BaseView.extend({
			tagName: 'li',
			className: 'has-dropdown',
			template: _.template(menuItemTemplate),
			initialize: function(options){
				options || (options = {});
				this.model = options.model || {};
			},
			render: function(){
				this.$el.empty();
				var data = this.model.toJSON();
				this.$el.append(this.template(data));
				return this;
			},

			events:{
				'click': 'showSubMenu'
			},

			showSubMenu: function(e, index){
				index || (index = null);
				var is_active = this.subViews[0].is_active();

				this.vent.trigger('menu:closeSubViews');
				this.$el.addClass('show');

				if (index !== null){
					this.subViews[0].subViews[index].activate();
				}else if(e && !e.isTrigger && !is_active){
					this.subViews[0].subViews[0].click();
				}
			},
			hideSubMenu: function(e){
				this.$el.removeClass('show');
			},
			is_active: function(){
				return this.$el.hasClass('show');
			}
		});

		return MenuItemView;

})