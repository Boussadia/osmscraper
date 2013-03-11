define([
	'jquery',
	'underscore',
	'backbone'
], function($,_, Backbone){
	var osm_brand = Backbone.Model.extend({
		defaults: {
			'name': 'Marque Brand',
			'osm': 'ooshop'
		},
		initialize: function(){
			return this;
		},
		cancel_match: function(){
			var id = this.get('id');
			var osm = this.get('osm');
			$.ajax({
				url: '/backend/matcher/'+osm+'/brand/cancel/'+id,
				type:"POST",
				dataType:"json",
				data:{},
				success: function(data, textStatus, jqXHR){
					console.log(data);
					console.log(textStatus);
					console.log(jqXHR);
				},
				error: function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);
				}
			});
		}
	});

	return osm_brand;

});