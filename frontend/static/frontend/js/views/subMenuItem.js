define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'text!../../templates/submenuitem.html'
	],function( $, _, Backbone, BaseView, subMenuItemTemplate){
		var MenuItemView = BaseView.extend({
			tagName: 'li',
			template: subMenuItemTemplate,
			initialize: function(options){
				options || (options = {});
				this.model = options.model || {};
			},
			render: function(){
				this.$el.empty();
				var template = _.template(this.template);
				var data = this.model.toJSON();
				// data['name'] = data['name'].toUpperCase();
				this.$el.append(template(data));
				return this;
			},

			events:{
				'click': 'showClick'
			},

			showClick: function(e){
				e.preventDefault();
				console.log(e.target);
			}
		});

		return MenuItemView;

})