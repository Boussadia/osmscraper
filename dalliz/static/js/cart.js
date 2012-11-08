$(document).ready(function(){
	// $('.add_to_cart').click(function(){
	// 	var product_id = $(this).data('product-id');
	// 	console.log(product_id);
	// 	$.ajax({
	// 		url:'/add/cart/',
	// 		type:"POST",
	// 		dataType:"json",
	// 		data:{
	// 			product_id: product_id,
	// 		},
	// 		success: function(data, textStatus, jqXHR){
	// 			console.log(data);
	// 			console.log(textStatus);
	// 			console.log(jqXHR);

	// 		},
	// 		error: function(jqXHR, textStatus, errorThrown){
	// 			console.log(jqXHR);
	// 			console.log(textStatus);
	// 			console.log(errorThrown);
	// 		}
	// 	});
	// });
	var PLUS_ONE_CLASS = 'add_one';
	var MINUS_ONE_CLASS = 'remove_one';

	$('.tocart').click(function(){
		if ($(this).attr('class').indexOf(PLUS_ONE_CLASS)>-1) {
			var quantity  = 1;
		}else{
			var quantity = -1;
		}
		var value_quantity = $($(this).parent().find('div.value_quantity')[0]);
		var value = parseFloat(value_quantity.text());
		if (value+quantity>0 && value+quantity<100){
			value_quantity.text(value+quantity);
			$($(this).parent().find('input.quantity')[0]).val(value+quantity);
		}
	});

	$('label[for="bin"]').click(function(){
		$(this).find('+input').click();
	})
})