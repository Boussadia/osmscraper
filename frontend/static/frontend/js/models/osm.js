define([
	'models/base'
	], function(BaseModel){

		var OsmModel = BaseModel.extend({
			defaults:{
				name: 'monoprix',
				price: 0,
				active: true
			},
			initialize: function(attributes, options){
				// Global events
				this.vent.on('carts', function(carts){
					var price = carts[this.get('name')].price;
					var active = carts[this.get('name')].active;
					this.set('price', price);
					this.set('active', active);
				},this);
				this.vent.on('osm', function(osm){
					var active = (osm.name === this.get('name') ? true : false );
					this.set('active', active);
				}, this);
			}
		});

		return OsmModel;

})