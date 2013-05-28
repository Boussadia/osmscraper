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
			sync: function(method, collection, options){
				if (method = 'read'){
					collection.each(function(osm){
						if (osm.active) this.vent.trriger('osm:current', osm.toJSON());
						if (osm.active) console.log(osm.toJSON());
					}, this)
				}
				return BaseCollection.prototype.sync.apply(this, [method, collection, options]);
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