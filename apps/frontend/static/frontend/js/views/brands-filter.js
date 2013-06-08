define([
	'underscore',
	'views/base',
	'text!../../templates/brands-filter.html',
], function(_, BaseView, brandsFilterTemplate){

	var BrandsFilterView = BaseView.extend({
		tagName: 'ul',
		className: 'brands',
		template: _.template(brandsFilterTemplate),
		initialize: function(options){
			this.brands = options.brands;
			this.category_id = options.category_id;
			this.selected_brand = [];
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var data = {'brands': this.brands};
			this.$el.append(this.template(data));
			return this;
		},
		events: {
			'click input[type=checkbox]': 'updateFilter'
		},
		updateFilter: function(e){
			this.selected_brand = [];
			var that = this;
			this.$el.find('input').each(function(i){
				var $input = $(this);
				var brand_id = parseInt($input.val());
				if ($input.is(':checked')) that.selected_brand.push(brand_id);
			})

			this.vent.trigger('brands:filter', {
				'brands': this.selected_brand,
				'id': this.category_id
			})
		}
	});
	return BrandsFilterView;
})