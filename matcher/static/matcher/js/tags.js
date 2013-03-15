$(document).ready(function(){

	// Product comments
	$('textarea.comment').bind('input propertychange', function(e) {
		var that = $(e.target);
		var comment = that.val();
		var product_id = that.attr('data-product');
		var osm = that.attr('data-osm');
		// Saving comment to server
		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/comment/'+product_id,
			type:"POST",
			dataType:"json",
			data:{
				'comment': comment
			},
			success: function(data, textStatus, jqXHR){
				console.log(data);
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
	});

	$('.tags').tagsInput({
		'removeWithBackspace' : false,
		onAddTag: function(tag){
		},
		onRemoveTag: function(tag){
		},
		onChange : function(x, y){
		},
		'interactive':false,
		'autocomplete_url': '/backend/tags/autocomplete/',
	});

	$('.cat').tagsInput({
		'removeWithBackspace' : false,
		'onAddTag': function(t){
		},
		'onRemoveTag': function(t){
		},
		'autocomplete_url': '/backend/tags/autocomplete/',
	});

});