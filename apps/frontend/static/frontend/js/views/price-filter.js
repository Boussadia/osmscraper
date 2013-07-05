define([
	'underscore',
	'views/base',
	'text!../../templates/price-filter.html',
], function(_, BaseView, priceFilterTemplate){

	var PriceFilterView = BaseView.extend({
		tagName: 'ul',
		className: 'price-filter',
		template: _.template(priceFilterTemplate),
		initialize: function(options){
			this.filters = options.filters;
			this.category_id = options.category_id;
			this.selected_filter = 0; // Default value of filter
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var data = {'filters': this.filters};
			this.$el.append(this.template(data));
			return this;
		},
		events: {
			'click a.cta': 'updateFilter',
			'click li': 'checkInput',
		},
		updateFilter: function(e){
			this.selected_filter = 0;
			var that = this;
			this.$el.find('input').each(function(i){
				var $input = $(this);
				var filter_id = parseInt($input.val());
				if ($input.is(':checked')) that.selected_filter = filter_id;
			})

			this.vent.trigger('price:filter', {
				'filter': this.selected_filter,
				'id': this.category_id
			})
			$(window).click();
		},
		checkInput: function(e){
			var $element = $(e.target);
			var input = $element.find('input');
			if(input) input.click();
		}
	});
	return PriceFilterView;
})