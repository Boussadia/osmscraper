define([
	'views/base',
	'text!../../templates/menuitem.html'
	],function(BaseView, menuItemTemplate){
		var MenuItemView = BaseView.extend({
			tagName: 'li',
			className: 'has-dropdown',
			template: menuItemTemplate,
			initialize: function(options){
				options || (options = {});
				this.model = options.model || {};
			},
			render: function(){
				this.$el.empty();
				var template = _.template(this.template);
				var data = this.model.toJSON();
				this.$el.append(template(data));
				return this;
			},

			events:{
				'click': 'showSubMenu'
			},

			showSubMenu: function(e){
				// e.preventDefault();
				this.vent.trigger('menu:closeSubViews');
				this.$el.addClass('show');
			},
			hideSubMenu: function(e){
				this.$el.removeClass('show');
			}
		});

		return MenuItemView;

})