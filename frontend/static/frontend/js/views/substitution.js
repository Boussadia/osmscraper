define([
	'underscore',
	'views/base',
	'text!../../templates/substitution.html'
], function(_, BaseView, substitutionTemplate){

	var SubstitutionView = BaseView.extend({
		template: _.template(substitutionTemplate),
		initialize: function(options){
			this.osms = options.osms;
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var data = this.product.toJSON();
			data['suggested'] = this.product.toJSON().osm_suggested_from;
			data['current'] = this.osms.get_active_osm().get('name');
			console.log(data);
			this.$el.append(this.template(data));
			var nb_products = this.$el.find('.products-container .product').length;
			var width_product = this.$el.find('.products-container .product').outerWidth();
			this.$el.find('.products-container').width(width_product*nb_products);
			return this;
		},
		events:{
			'click .equivalent-switch-bg': 'hide',
			'click a.osms-switch-close': 'hide',
		},
		hide: function(e){
			this.$el.hide();
		}

	});


	return SubstitutionView;

})