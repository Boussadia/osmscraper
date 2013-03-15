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

	// Tags
	$('.tags').tagsInput({
		'removeWithBackspace' : false,
		onAddTag: function(tag){
			save_tags($(this));
		},
		onRemoveTag: function(tag){
			save_tags($(this));
		},
		onChange : function(x, y){
		},
		'autocomplete_url': '/backend/tags/autocomplete/',
	});

	// Catégories
	$('.cat').tagsInput({
		'removeWithBackspace' : false,
		'onAddTag': function(t){
		},
		'onRemoveTag': function(t){
		},
		'autocomplete_url': '/backend/tags/autocomplete/',
	});

	// Function that saves tags
	var save_tags = function(input){
		var id_product = input.attr('data-product');
		var osm = input.attr('data-osm');
		var tags_string = input.val();
		if (tags_string === '') tags_string = ',';
		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/set/'+id_product+'/'+tags_string,
			type:"POST",
			dataType:"json",
			data:{},
			success: function(data, textStatus, jqXHR){
				console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
	}

});