define([
	'models/cart'
], function(CartModel){

	var SuggestedCartModel = CartModel.extend({
		initialize: function(attributes, options){
			CartModel.prototype.initialize.apply(this, [attributes, options]);
			this.osms.on('change', function(osm){
				if(!this.get('name') && !osm.get('active')){
					this.set('name', osm.get('name'));
					this.fetch();
				}else if(this.get('name') && osm.get('active') && this.get('name') === osm.get('name')){
					var unactive_osm = this.osms.find(function(osm){
						return !osm.get('active');
					});
					this.set('name', unactive_osm.get('name'));
					this.fetch();
				}
			}, this);
		},
		fetch: function(options){
			options = options ? _.clone(options) : {};
			options.data = {
				'osm_name': this.get('name')
			}
			return CartModel.prototype.fetch.apply(this, [options]);
		}
	});


	return SuggestedCartModel;

})