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
				// e.preventDefault();
				index || (index = null);
				this.vent.trigger('menu:closeSubViews');
				this.$el.addClass('show');

				if (index !== null){
					this.subViews[0].subViews[index].activate();
				}
			},
			hideSubMenu: function(e){
				this.$el.removeClass('show');
			}
		});

		return MenuItemView;

})