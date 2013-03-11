define([
	'jquery',
	'underscore',
	'backbone'
], function($,_, Backbone){
	var Ooshop_brand = Backbone.Model.extend({
		defaults: {
			'name': 'Marque Ooshop'
		},
		initialize: function(){
			return this;
		},
		cancel_match: function(){
			var id = this.get('id');

			$.ajax({
				url: '/brand/ooshop/cancel/'+id,
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

	return Ooshop_brand;

});