define([
	'underscore',
	'views/base',
	'text!../../templates/submenuitem.html'
	],function(_, BaseView, subMenuItemTemplate){
		var MenuItemView = BaseView.extend({
			tagName: 'li',
			template: subMenuItemTemplate,
			activateClass: 'active',
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
			click: function(){
				this.$el.find('a').click();
			},
			activate: function(){
				this.$el.find('p').addClass(this.activateClass);
			},
			unactivate: function(){
				this.$el.find('p').removeClass(this.activateClass);
			}
		});

		return MenuItemView;

})