define([
	'underscore',
	'jquery',
	'backbone',
	'views/baseView'
	], function(_, $, Backbone, BaseView){
		var CategoryView = BaseView.extend({
			template: $('#template_category').text(),
			initialize: function(option){
				this.model = option.model || {};
				return this;
			},
			render: function(){
				var template = _.template(this.template);
				this.el = template(this.model.toJSON());
				return this;
			}
		});
		return CategoryView;

})