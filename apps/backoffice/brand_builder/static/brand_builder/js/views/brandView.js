define([
	'underscore',
	'jquery',
	'backbone',
	'views/baseView'
	], function(_, $, Backbone, BaseView){
		var BrandView = BaseView.extend({
			template: $('#template_brand').text(),
			initialize: function(option){
				this.model = option.model || {};
				this.is_current = option.is_current || false;
				return this;
			},
			render: function(){
				var template = _.template(this.template);
				var data = this.model.toJSON();
				data['class_current'] = this.is_current ? 'current' : '';
				this.el = template(data);
				return this;
			},
			set_current: function(bool){
				this.is_current = bool;
			}
		});
		return BrandView;

})