define([
	'underscore',
	'collections/base',
	'models/osm'
	], function(_, BaseCollection, OsmModel){

		var OsmsCollections = BaseCollection.extend({
			url:'/api/osm',
			model: OsmModel,
			initialize: function(){
				this.vent.on('carts', function(carts){
					// var price = carts[this.get('name')].price;
					// console.log(this);
					// console.log(carts);
					// this.set('price', price);
				},this);
			},
			sync: function(method, collection, options){
				if (method = 'read'){
					collection.each(function(osm){
						if (osm.active) this.vent.trriger('osm:current', osm.toJSON());
						if (osm.active) console.log(osm.toJSON());
					}, this)
				}
				return BaseCollection.prototype.sync.apply(this, [method, collection, options]);
			}
		});

		return OsmsCollections;
})