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
			this.$el.append(this.template(data));
			var nb_products = this.$el.find('.products-container .product').length;
			var width_product = this.$el.find('.products-container .product').outerWidth();
			this.$el.find('.products-container').width(width_product*nb_products);
			return this;
		},
		events:{
			'click .equivalent-switch-bg': 'hide',
			'click a.osms-switch-close': 'hide',
			'click a.substitute': 'substitute',
		},
		hide: function(e){
			this.$el.hide();
		},
		substitute: function(e){
			var that = this;
			var content_id = this.product.get('id');
			var $target = $(e.target);
			var reference_selected = $target.attr('data-reference');

			options = {
				'content_id': content_id,
				'reference_selected': reference_selected,
				'osm_selected': this.osms.get_active_osm().get('name')
			}

			_.extend(options, {
				'substitute': true,
				'success': function(){
					that.hide();
					
				}
			});

			this.product.save(null, options);
		}

	});


	return SubstitutionView;

})