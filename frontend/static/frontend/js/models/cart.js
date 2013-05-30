define([
	'models/base'
	], function(BaseModel){

		var CartModel = BaseModel.extend({
			url: '/api/cart',
			initialize: function(attributes, options){
				this.osms = options.osms;
				this.set_suggested();
				this.vent.on('cart:newproduct', this.fetch, this);

				this.osms.on('change add', function(osm){
					if(osm.get('active') &&  this.get('name') !== osm.get('name')){
						this.set('name', osm.get('name'));
						this.set_suggested();
						this.fetch();
					}else if(!osm.get('active') &&  this.get('name') === this.suggested){
						this.set_suggested(osm.get('name'))

					}
				}, this);
				
			},
			parse: function(resp, xhr){
				return resp;
			},
			set_suggested: function(suggested){
				if(!suggested){
					var unactive_osm = this.osms.find(function(osm){
						return !osm.get('active');
					});
					if (unactive_osm) this.suggested =  unactive_osm.get('name') || 'monoprix';
					if (!unactive_osm) this.suggested =  'monoprix';

				}else{
					this.suggested = suggested;
				}

				if (this.suggested === this.get('name')) this.set_suggested();
			}
		})

		return CartModel;

})