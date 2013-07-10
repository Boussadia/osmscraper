define([
	'models/base',
	'collections/searchresults'
	], function(BaseModel, SearchResultsCollection){

		var Search = BaseModel.extend({
			url: '/api/search',

			initialize: function(){
				this.results = new SearchResultsCollection( this.get( "results" ) );
				this.trigger( "search:ready", this );
			},

			parse: function(response, options){
				this.results = response
			}

		});


		return Search;
})