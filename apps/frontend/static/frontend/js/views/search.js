define([
	'jquery',
	'views/base',
	'models/search',
	'typeahead'
	], function($, BaseView, SearchModel){

		var SearchView = BaseView.extend({
			el: $('input#search'),
			initialize: function(options){
				options || (options = {});

				// Initializing typeahead
				this.$el.typeahead([
					{
						name: 'products-sugestion',
						local: [],
						remote: '/api/autocomplete/products/%QUERY',
						header: '<h3 class="league-name">Produits</h3>'
					},
					{
						name: 'brands-sugestion',
						local: [],
						remote: '/api/autocomplete/brands/%QUERY',
						header: '<h3 class="league-name">Marques</h3>'
					}
				]);
			},
			events:{
				'keypress': 'do_search'
			},
			do_search: function(e){
				if (e.keyCode === 13){
					// Pressing enter -> performing search
					this.search_model = new SearchModel({
						text: this.$el.val()
					},
					{
						'vent': this.vent
					});
					var that = this;

					this.search_model.save(null, {
						attrs: {
							text: this.$el.val()
						}
					});
				}
			},
			render: function(resutls){
			}

		});

		return SearchView;

})