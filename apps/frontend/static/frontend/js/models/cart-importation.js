define([
	'models/base'
	], function(BaseModel){

		var CartImportationModel = BaseModel.extend({
			url: '/api/cart/importation',
			defaults:{
				'email': 'ahmed.boussadia@hotmail.fr',
				'password': '2asefthukom,3'
			},
			initialize: function(attributes, options){
				
			},
			parse: function(resp, xhr){
				return resp.test;
			},
			save: function(attributes, options){
				attributes || (attributes = {});
				var email = attributes.email || this.get('email');
				var password = attributes.password || this.get('password');
				var osm = attributes.osm || this.get('osm');
				
				options || (options = {});
				var vent = this.vent;
				var that = this;

				options.emulateJSON = true;
				options.data = {
					'email': email,
					'password': password,
					'osm_name': osm
				};

				var that = this;

				options.success = function(){
					
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		})

		return CartImportationModel;

})