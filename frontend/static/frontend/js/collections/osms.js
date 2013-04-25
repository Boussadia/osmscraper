define([
	'underscore',
	'collections/base',
	'models/osm'
	], function(_, BaseCollection, OsmModel){

		var OsmsCollections = BaseCollection.extend({
			model: OsmModel,
			initialize: function(){
				// _.each(['auchan', 'monoprix', 'ooshop'], function(osm_name){
				// 	var osm = new OsmModel({ name: osm_name}, {'vent': this.vent} );
				// 	this.push(osm);
				// 	console.log(osm);
				// }, this);
			}
		});

		return OsmsCollections;
})