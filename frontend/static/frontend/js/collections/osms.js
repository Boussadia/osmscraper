define([
	'underscore',
	'collections/base',
	'models/osm'
	], function(_, BaseCollection, OsmModel){

		var OsmsCollections = BaseCollection.extend({
			url:'/api/osm',
			model: OsmModel,
			initialize: function(){
			},
			get_active_osm: function(){
				var active_osm = _.find(this.models, function(osm, i){
					return osm.get('active');
				}, this);
				return active_osm;
			}
		});

		return OsmsCollections;
})