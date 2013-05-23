define([
	'models/base'
	], function(BaseModel){

		var OsmModel = BaseModel.extend({
			url:'/api/osm',
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
					if(active) this.vent.trigger('osm', this.toJSON());
				},this);

				this.vent.on('osm', function(osm){
					var active = (osm.name === this.get('name') ? true : false );
					this.set('active', active);
				}, this);
			},
			save: function(attributes, options){
				attributes || (attributes = {});
				options || (options = {});
				var vent = this.vent;
				var that = this;
				options.emulateJSON = true;

				options.data = {
					'new_name': this.get('name')
				}
				options.success = function(data, textStatus, jqXHR){
					
					// that.vent.trigger('route:category:force');
				}

				options.error = function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			},
			parse: function(resp, xhr){
				return resp.osm;
			}
		});

		return OsmModel;

})