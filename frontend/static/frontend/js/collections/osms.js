define([
	'underscore',
	'collections/base',
	'models/osm'
	], function(_, BaseCollection, OsmModel){

		var OsmsCollections = BaseCollection.extend({
			model: OsmModel,
			initialize: function(){
				this.vent.on('carts', function(carts){
					// var price = carts[this.get('name')].price;
					// console.log(this);
					// console.log(carts);
					// this.set('price', price);
				},this);
			}
		});

		return OsmsCollections;
})