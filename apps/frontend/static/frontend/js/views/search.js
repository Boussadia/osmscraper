define([
	'jquery',
	'views/base',
	'models/search'
	], function($, BaseView, SearchModel){

		var SearchView = BaseView.extend({
			el: $('input#search'),
			initialize: function(options){
				options || (options = {});
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