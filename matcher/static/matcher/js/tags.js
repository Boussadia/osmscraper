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

	// Categories
	$('.cat').tagsInput({
		'removeWithBackspace' : false,
		'onAddTag': function(t){
			save_categories($(this));
		},
		'onRemoveTag': function(t){
			save_categories($(this));
		},
		'autocomplete_url': '/backend/matcher/tags/categorie/autocomplete/',
		'delimiter': '|',
	});

	// Merge button
	$('button.merge').click(function(e){
		$that = $(this);
		var osm = $that.attr('data-osm');
		var product = $that.attr('data-product');
		var osm_from = $that.attr('data-osm_from');
		var product_from = $that.attr('data-product_from');

		console.log([osm, osm_from, product, product_from]);
		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/match/'+osm_from+'/'+product+'/'+product_from,
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
		
	})
	// UnMerge button
	$('button.unmerge').click(function(e){
		$that = $(this);
		var osm = $that.attr('data-osm');
		var product = $that.attr('data-product');
		var osm_from = $that.attr('data-osm_from');
		var product_from = $that.attr('data-product_from');

		console.log([osm, osm_from, product, product_from]);
		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/match/'+osm_from+'/'+product+'/'+product_from,
			type:"DELETE",
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
		
	})

	// Les zones matchées
	$( ".accordion" ).accordion({
      collapsible: true,
      active: false,
      heightStyleType: 'content'
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

	// Function that saves categories
	var save_categories = function(input){
		var categories_str = input.val();
		id_categories = [];
		if (categories_str !== ""){
			var categories = categories_str.split('|');
			for(var i = 0; i<categories.length; i++){
				var splitted = categories[i].split(' - ');
				var last = splitted.length-1
				id_categories.push(parseInt(splitted[last]));
			}
		}
		var id_product = input.attr('data-product');
		var osm = input.attr('data-osm');
		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/categorie/set/'+id_product,
			type:"POST",
			dataType:"json",
			data:{
				"categories": id_categories,
			},
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