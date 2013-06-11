define([
	'underscore',
	'views/base',
	'text!../../templates/order.html'
], function(_, BaseView, orderTemplate){

	var OrderView = BaseView.extend({
		template: _.template(orderTemplate),
		initialize: function(options){
			this.osms = options.osms;
			this.bindTo(this.osms, 'change', this.render);
		},
		render: function() {
			this.closeSubViews();
			this.$el.empty();
			var data = this.osms.get_active_osm().toJSON();
			this.$el.append(this.template(data));
			return this;
		}
	});

	return OrderView;
})