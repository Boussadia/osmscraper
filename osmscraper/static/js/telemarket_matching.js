$(document).ready(function(){
	$('#start').click(function(){
		window.location.hash = first_element_id;
	})

	$('html').keyup(function(e){
		if(e.keyCode==17){
			next();
		}
	});

	$("#next").click(function(){
		next();
	});

	$("#previous").click(function(){
		previous();
	});

	$('#cancel').click(function(){
		$('#loading').show();
		$('#main').addClass('loading');
		var id_telemarket = $('#telemarket').attr('data-id');
		$.ajax({
			url:'/telemarket_monoprix/products/cancel/'+id_telemarket,
			type:"POST",
			dataType:"json",
			data:{},
			beforeSend: function(jqXHR, settings){
				// console.log(jqXHR);
				// console.log(settings);
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);
				$('#loading').hide();
				$('#main').removeClass('loading');
				$('.selected').removeClass('selected');
				

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});

	})

	// Hash change handling
	var current_hash = "";
	setInterval(function(){
		var new_hash = window.location.hash;
		if (new_hash !== current_hash) {
			current_hash = new_hash;
			var id = parseInt(current_hash.substring(1));
			if (!isNaN(id)){
				$('#telemarket').attr('data-id', id);
				get_data(id);
				ID_TELEMARKET_PRODUCT = id;

			}
		};
	},100);

	// Getting data from server
	get_data = function(id){
		$('#loading').show();
		$('#main').addClass('loading');
		ID_TELEMARKET_PRODUCT = id;

		$('#start').hide();
		$('#main').show();
		$.ajax({
			url:'/telemarket_monoprix/products/suggestions/'+id,
			type:"GET",
			dataType:"json",
			data:{},
			beforeSend: function(jqXHR, settings){
				// console.log(jqXHR);
				// console.log(settings);
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);
				set_html_telemarket_product(data['product']);
				set_suggestions_html(data['suggestions']);
				set_selected(data['product']['monoprix_product'], id);
				$('#loading').hide();
				$('#main').removeClass('loading');
				

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	}

	// Filling telemarket product function
	set_html_telemarket_product = function(telemarket_product){
		var name_product = telemarket_product['title'];
		var url_photo = telemarket_product['image_url'];
		var url_product = 'http://telemarket.fr'+telemarket_product['url'];
		var categories = telemarket_product['categories'];
		var text_categories = 'Categories : ';
		for (var i = 0; i<categories.length; i++){
			text_categories = text_categories +categories[i]['name'];
			if (i===categories.length-1) {
				text_categories = text_categories +'.';
			}else{
				text_categories = text_categories +', ';
			}
		}
		text_categories = text_categories+' | price = '+telemarket_product['price']+'€ | unit price '+telemarket_product['unit_price']+'€/unit';
		ID_TELEMARKET_PRODUCT = telemarket_product['id'];

		$('#telemarket .name_product').text(name_product);
		$('#telemarket .categories').text(text_categories);
		$('#telemarket a.link_product').attr("href",url_product);
		$('#telemarket img.product_image').attr("src",url_photo);

	}

	// Setting active product match and post data to server
	set_selected = function(id_monoprix, id_telemarket){
		var id = null;


		if (id_monoprix === null) {
		// 	var ids = $('.monoprix');
		// 	if(ids.length>0){
		// 		var id = $(ids[0]).attr("data-id");
		// 	}
		// }else{
			id = id_monoprix;
		}else{
			id = id_monoprix;
		}

		if(id !== null){
			$('.selected').removeClass('selected');
			$('.monoprix[data-id='+id+']').addClass('selected');
			$.ajax({
				url:'/telemarket_monoprix/products/suggestions/'+id_telemarket,
				type:"POST",
				dataType:"json",
				data:{
					'id_monoprix': id
				},
				beforeSend: function(jqXHR, settings){
					// console.log(jqXHR);
					// console.log(settings);
				},
				success: function(data, textStatus, jqXHR){
					// console.log(data);
					// console.log(textStatus);
					// console.log(jqXHR);
					

				},
				error: function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);

					// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
				}
			});
		}

	}

	// Filling suggestions
	set_suggestions_html = function(suggestions){
		$("#suggestions .container").empty();
		for(var i = 0; i<suggestions.length; i++){
			var div = get_template_product_monoprix(suggestions[i]);
			$("#suggestions .container").append(div);
		}

	}

	get_template_product_monoprix = function(product){
		var id_telemarket = $('#telemarket').attr('data-id');
		var name_product = product['product_name'];
		var url_photo = 'http://courses.monoprix.fr/'+product['image_url'];
		var brand_name = product['brand_name'];
		var url_product = 'http://courses.monoprix.fr/'+product['url'];
		var id = product['id'];

		var div = $('<div>').addClass('monoprix').attr('data-id',id);
		var h3 = $('<h3>').addClass('name_product').text(name_product);
		var h4 = $('<h3>').addClass('brand_name').text(brand_name);
		var a = $('<a>').addClass('link_product').attr('target','_blank').attr("href",url_product);
		var div_unit_price = $('<p>').addClass('unit_price').text(product['price']+' € | '+product['unit_price']+' €/'+product['unit']+' | '+Math.round(product['price']/product['unit_price']*100)/100+' '+product['unit'])
		var img = $('<img>').addClass('product_image').attr("src",url_photo);
		var button = $('<button>').addClass('set_match').text('Select this product.');
		button.click(function(){
			set_selected(id, id_telemarket);
		})
		a.append(img);
		div.append(h3);
		div.append(h4);
		div.append(div_unit_price);
		div.append(a);
		div.append(button);
		return div;
	}

	// Go to next product
	next = function(){
		var id_telemarket = $('#telemarket').attr('data-id');

		$.ajax({
			url:'/telemarket_monoprix/products/next/'+id_telemarket,
			type:"GET",
			dataType:"json",
			data:{},
			beforeSend: function(jqXHR, settings){
				// console.log(jqXHR);
				// console.log(settings);
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);
				if (data['status'] == 200){
					window.location.hash = data['id']
				}
				

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	}

	// Go to next product
	previous = function(){
		var id_telemarket = $('#telemarket').attr('data-id');

		$.ajax({
			url:'/telemarket_monoprix/products/previous/'+id_telemarket,
			type:"GET",
			dataType:"json",
			data:{},
			beforeSend: function(jqXHR, settings){
				// console.log(jqXHR);
				// console.log(settings);
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);
				if (data['status'] == 200){
					window.location.hash = data['id']
				}
				

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	}
})