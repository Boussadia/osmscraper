define([
	'jquery',
	'underscore',
	'backbone',
	'views/base',
	'views/subMenuItem',
	'collections/subMenu'
	], function($, _, Backbone, BaseView, SubMenuItemView, SubMenuCollection){

		var SubMenuView = BaseView.extend({
			tagName: 'ul',
			className: 'dropdown',
			initialize: function(options){
				options || (options = {});
				this.models = options.models || {};
				this.subMenuCollection = new SubMenuCollection(this.models, {'vent': this.vent});
				// this.bindTo(this.subMenuCollection, 'reset', function(a, b){
				// 	this.render();
				// }, this);
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				this.subMenuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this)
				return this;
			},
			addOne: function(menuItem){
				var view = new SubMenuItemView({'model':menuItem});
				this.addSubView(view);
				this.$el.append(view.render().el);
			}
		});

		return SubMenuView;
})