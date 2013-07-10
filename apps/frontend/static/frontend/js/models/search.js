define([
	'models/base',
	'collections/searchresults'
	], function(BaseModel, SearchResultsCollection){

		var Search = BaseModel.extend({
			url: '/api/search',

			initialize: function(){
			},

			parse: function(response, options){
				// Setting search result in collection
				this.results = new SearchResultsCollection( response , {'vent': this.vent});
				this.vent.trigger('search:results', {
					'results':this.results
				});
				return this.toJSON();
			}

		});


		return Search;
})