$(document).ready(function(){
	// Filter by brand
	$("input:checkbox[name=brands_options]").click(function() {
		if (parseInt($(this).val()) === 0) {
			if($(this).is(':checked')){
				$("input:checkbox[name=brands_options]:not([id='brand_0'])").prop('checked',false);
			}
		}else{
			$($("input:checkbox[name=brands_options][id='brand_0']")[0]).prop('checked',false);
		}
		var all_is_checked = $($("input:checkbox[name=brands_options][id='brand_0']")[0]).is(':checked');
		// var brands_checked = $("input:checkbox[name=brands_options]:checked:not([id='brand_0'])").length;
		if (all_is_checked) {
			$('.product').show()
		}else{
			$('.product').hide();
			$("input:checkbox[name=brands_options]:not([id='brand_0'])").each(function(){
				var id_brand = $(this).val();
				if ($(this).is(':checked')) {
					$('.product[data-brand='+id_brand+']').show();
				}else{
					$('.product[data-brand='+id_brand+']').hide();
				}
			})
		}
	});

	// Filter by price
	function filter_by_price_low_to_high(products){
		var sorted_products = products;
		var sorted = false;
		while(!sorted){
			sorted = true;
			for (var i=0; i<products.length-1; i++){
				// console.log(($(products[i]).attr('data-price')));
				// console.log(($(products[i+1]).attr('data-price')));

				if( parseFloat( $(products[i]).attr('data-price') ) > parseFloat( $(products[i+1]).attr('data-price') ) ) {
					temp_i = products[i];
					temp_i1 = products[i+1];
					sorted_products[i] = temp_i1;
					sorted_products[i+1] = temp_i;
					sorted = false;
					break;
				}
			}
			products = sorted_products;
		}
		return products;

		// products.each(function(){$('.products').append($(this))})
	}

	// Filter by price
	function filter_by_price_high_to_low(products){
		$.fn.reverse = [].reverse;
		return filter_by_price_low_to_high(products).reverse();
	}

	// Events handlers:
	$('#prix_croissant').click(function(){
		$("#text_filter").html($(this).text()+'<b class="caret"></b>');
		var products = $('.product:visible');
		$('.product:visible').remove();
		products = filter_by_price_low_to_high(products);
		products.each(function(){$('.products').append($(this))})
	});

	$('#prix_decroissant').click(function(){
		$("#text_filter").html($(this).text()+'<b class="caret"></b>');
		var products = $('.product:visible');
		$('.product:visible').remove();
		products = filter_by_price_high_to_low(products);
		products.each(function(){$('.products').append($(this))})
	});

	// Number of products init
	$("input[id^='brand_']").each(function(){
		$that = $(this)
		var id = $that.data('id');
		$products = $('.product')
		if (id===0){
			var count = $products.length
			$that.find("+label").html($that.find("+label").text()+' <span>('+count+')</span>');			
		}else{
			var count = $('div[data-brand='+id+']').length
			$that.find("+label").html($that.find("+label").text()+' <span>('+count+')</span>');
		}
	})
});