$(document).ready(function(){
	var category_areas = $('.category_area').each(function(){
		var has_no_match = $(this).find('.has_no_match').remove();
		$(this).prepend(has_no_match);
		has_no_match.accordion({
			collapsible: true,
			active: false,
			heightStyleType: 'content'
		});

		var not_category = $(this).find('.category_is_not_set:not(.has_no_match)').remove();
		$(this).append(not_category);

		not_category.accordion({
			collapsible: true,
			active: false,
			heightStyleType: 'content'
		});
		var matched = $(this).find('.match_is_set:not(.category_area):not(.has_no_match)').remove();
		$(this).prepend(matched);

		matched.accordion({
			collapsible: true,
			active: false,
			heightStyleType: 'content'
		});
	});

	// Go to category page
	fill_select('first', dalliz_categories);
	set_sub_categories('first', main_category);
	if (main_category !== parent_category) set_sub_categories('second', parent_category);
	// if (parent_category !== category) set_sub_categories('third', category);

	function fill_select(id_element, categories){
		$(".add select#"+id_element).empty();
		for (id in categories){
			name = categories[id]['name'];
			$(".add select#"+id_element).append(
				$("<option>").text(name).val(id)
			)
		}

		$(".add select#"+id_element).change(function(){
			id_category = $(".add select#"+id_element).find(":selected").val()
			set_sub_categories(id_element, id_category)
		})

	}

	function set_sub_categories(id_element, id_category){
		$(".add select#"+id_element+" option[value="+id_category+"]").attr('selected', true);
		if (id_element === "first"){
			fill_select('second', dalliz_categories[id_category]['subs']);
			id_category_second = $(".add select#second").find(":selected").val();
			// if (dalliz_categories[id_category]['subs'][id_category_second]){
			// 	fill_select('third', dalliz_categories[id_category]['subs'][id_category_second]['subs'])
			// }
		} //else if(id_element === "second"){
		// 	id_category_first = $(".add select#first").find(":selected").val();
		// 	fill_select('third', dalliz_categories[id_category_first]['subs'][id_category]['subs'])
		// }
	}

	$('#go').click(function(){
		var id_category = $(".add select#second").find(":selected").val();

		if (id_category !== undefined) window.location = '/backend/matcher/'+osm+'/tags/'+id_category;
	})

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
	var options_tags = {
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
	};
	$('.tags').tagsInput(options_tags);

	// Categories
	var options_categories = {
		'removeWithBackspace' : false,
		'onAddTag': function(t){
			save_categories($(this));
		},
		'onRemoveTag': function(t){
			save_categories($(this));
		},
		'autocomplete_url': '/backend/matcher/tags/categorie/autocomplete/',
		'delimiter': '|',
	};
	$('.cat').tagsInput(options_categories);

	// Merge button
	$('button.merge').bind('click', merge);

	function merge(e){
		$that = $(e.target);
		var osm = $that.attr('data-osm');
		var product = $that.attr('data-product');
		var osm_from = $that.attr('data-osm_from');
		var product_from = $that.attr('data-product_from');

		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/match/'+osm_from+'/'+product+'/'+product_from,
			type:"POST",
			dataType:"json",
			data:{},
			success: function(data, textStatus, jqXHR){
				var categories = data['categories'];
				var tags = data['tags'];
				var matched_area = $('.product[data-product='+product+'][data-osm='+osm+'] .matched_area');
				var merged_product = $('.product[data-product='+product+'][data-osm='+osm+'] .unmatched[data-product_from='+product_from+'][data-osm_from='+osm_from+']').remove();
				merged_product.appendTo(matched_area);
				merged_product.removeClass('unmatched')
								.addClass('matched')
								.accordion({
									collapsible: true,
									active: false,
									heightStyleType: 'content'
								})
									.find('button')
										.unbind('click')
										.text('Cancel')
										.removeClass('merge')
										.addClass('unmerge')
										.click(unmerge);
				merged_product.find('input').val('');
				merged_product.find('.cat + div').remove();
				for (var i  = 0; i<categories.length; i++){
					if(i > 0){
						merged_product.find('input.cat').val(merged_product.find('input.cat').val()+'|'+categories[i]['name']+' - '+categories[i]['id']);
					}else{
						merged_product.find('input.cat').val(categories[i]['name']+' - '+categories[i]['id']);
					}
				}
				merged_product.find('.cat').tagsInput(options_categories);
				merged_product.find('.tags + div').remove();
				for (var i  = 0; i<tags.length; i++){
					if(i > 0){
						merged_product.find('input.tags').val(merged_product.find('input.tags').val()+','+tags[i]['name']);
					}else{
						merged_product.find('input.tags').val(tags[i]['name']);
					}
				}
				merged_product.find('.tags').tagsInput(options_tags);
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
		
	}
	// UnMerge button
	$('button.unmerge').bind('click', unmerge);

	function unmerge(e){
		$that = $(e.target);
		var osm = $that.attr('data-osm');
		var product = $that.attr('data-product');
		var osm_from = $that.attr('data-osm_from');
		var product_from = $that.attr('data-product_from');

		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/match/'+osm_from+'/'+product+'/'+product_from,
			type:"DELETE",
			dataType:"json",
			data:{},
			success: function(data, textStatus, jqXHR){
				var categories = data['categories'];
				var tags = data['tags'];

				var unmatched_area = $('.product[data-product='+product+'][data-osm='+osm+'] .unmatched_area');
				var unmerged_product = $('.product[data-product='+product+'][data-osm='+osm+'] .matched[data-product_from='+product_from+'][data-osm_from='+osm_from+']').accordion( "destroy" );
				unmerged_product.removeClass('matched')
								.addClass('unmatched')
								.find('button')
										.text('Merge')
										.unbind('click')
										.removeClass('unmerge')
										.addClass('merge')
										.bind('click', merge);
				unmerged_product.appendTo(unmatched_area);
				// unmerged_product.find('.cat + div').remove();
				// unmerged_product.find('.cat').tagsInput(options_categories);
				// unmerged_product.find('.tags + div').remove();
				// unmerged_product.find('.tags').tagsInput(options_tags);

				unmerged_product.find('input').val('');
				unmerged_product.find('.cat + div').remove();
				for (var i  = 0; i<categories.length; i++){
					if(i > 0){
						unmerged_product.find('input.cat').val(unmerged_product.find('input.cat').val()+'|'+categories[i]['name']+' - '+categories[i]['id']);
					}else{
						unmerged_product.find('input.cat').val(categories[i]['name']+' - '+categories[i]['id']);
					}
				}
				unmerged_product.find('.cat').tagsInput(options_categories);
				unmerged_product.find('.tags + div').remove();
				for (var i  = 0; i<tags.length; i++){
					if(i > 0){
						unmerged_product.find('input.tags').val(unmerged_product.find('input.tags').val()+','+tags[i]['name']);
					}else{
						unmerged_product.find('input.tags').val(tags[i]['name']);
					}
				}
				unmerged_product.find('.tags').tagsInput(options_tags);

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
		
	}

	// Les zones matchées
	$( ".matched_area .matched" ).accordion({
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

	// Set product has no similarity
	$('button.nogood').click(function(e){
		$that = $(e.target);
		var osm = $that.attr('data-osm');
		var product = $that.attr('data-product');
		var osm_from = $that.attr('data-osm_from');
		var product_from = $that.attr('data-product_from');

		$.ajax({
			url:'/backend/matcher/'+osm+'/tags/nosimilarity/'+osm_from+'/'+product+'/'+product_from,
			type:"POST",
			dataType:"json",
			data:{},
			success: function(data, textStatus, jqXHR){
				console.log(data)
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
	})

});