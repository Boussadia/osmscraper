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
					console
					this.search = new SearchModel({
						text: this.$el.val()
					});
					var that = this;
					this.bindTo(this.search, 'search:ready', function(results){
						that.render(results);
					});

					this.search.save(null, {
						attrs: {
							text: this.$el.val()
						}
					});
				}
			},
			render: function(resutls){
				console.log(resutls);
			}

		});

		return SearchView;

})