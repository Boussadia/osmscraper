define([
	'underscore',
	'views/base',
	'text!../../templates/order.html'
], function(_, BaseView, orderTemplate){

	var OrderView = BaseView.extend({
		template: _.template(orderTemplate),
		initialize: function(options){
			this.data = {
				price: 0,
				name: 'monoprix',
				minimum: 70
			}
			this.data = options.data || this.data;
		},
		render: function() {
			this.$el.empty();
			this.$el.append(this.template(this.data));
			return this;
		}
	});

	return OrderView;
})