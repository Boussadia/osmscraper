define([
	'jquery',
	'underscore',
	'backbone'
], function($,_, Backbone){
	var Match = Backbone.Model.extend({
		defaults: {
			'name': 'Marque Dalliz',
			'id': -1,
			'score': 0,
			'is_match': false
		},
		initialize: function(){
			return this;
		},
		set_match: function(id_ooshop_brand){
			var dalliz_brand_id = this.get('id');

			$.ajax({
				url: '/brand/ooshop/set/'+id_ooshop_brand+'/'+dalliz_brand_id,
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

	return Match

});