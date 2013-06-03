define([
	'underscore',
	'jquery',
	'backbone',
	'views/baseView'
	], function(_, $, Backbone, BaseView){
		var CategoryView = BaseView.extend({
			template: $('#template_category').text(),
			tagName: 'tr',
			className: 'category',
			attributes: function(){
				return {
					'data-id': this.model.id
				}
			},
			initialize: function(option){
				this.model = option.model || {};
				this.is_current = option.is_current || false;
				this.bindTo(this.model, 'change', this.render);
				return this;
			},
			render: function(){
				this.$el.empty();
				var template = _.template(this.template);
				var data = this.model.toJSON();
				data['class_current'] = this.is_current ? 'current' : '';
				this.$el.append(template(data));

				return this;
			},
			set_current: function(bool){
				this.is_current = bool;
			},
			events: {
				'change input.name': 'changeName',
				'keypup input.name': 'changeName',
				'keypress input.name': 'changeName',
				'change input.position': 'changePosition',
			},
			changePosition: function(e){
				this.model.savePosition(this.$el.find('input.position').val());
			},
      changeName: function(e){
        this.model.saveName(this.$el.find('input.name').val());
      }
		});
		return CategoryView;

})
