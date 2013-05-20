define([
	'underscore',
	'views/base',
	'text!../../templates/category-in-cart.html'
	], function(_, BaseView, categoryInCartTemplate){

		var CategoryInCartView = BaseView.extend({
			template: _.template(categoryInCartTemplate),
			initialize: function(options){
				options || (options = {});
				this.data = options.content;

			},
			render: function(){
				this.$el.empty();
				var data = this.data;
				this.$el.append(this.template(data));
				return this;
			}
		});

		return CategoryInCartView;
});