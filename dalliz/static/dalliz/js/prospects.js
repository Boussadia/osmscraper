$(document).ready(function(){
	$('#modalProspect').keypress(function(e){
		var code = e.charCode;
		if (code === 13) {
			$('#send_mail').trigger('click');
		};
	})

	$('#send_mail').click(function(){
		var mail = $('.mail').val();
		send_mail_prospect(mail);
	});
});


function send_mail_prospect(mail){
	var mail_validator = /\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/i;
	if (mail_validator.test(mail)) {
		$.ajax({
			url:'/prospects',
			type:"POST",
			dataType:"json",
			data:{
				"mail" : mail,
			},
			error: function(jqXHR, textStatus, errorThrown){
				// console.log(jqXHR);
				// console.log(textStatus);
				// console.log(errorThrown);
				$('.successmessage, .errormessage').hide();
				$('.smth-wrong').fadeIn();
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(jqXHR);
				// console.log(textStatus);
				$('.successmessage, .errormessage').hide();
				$('.successmessage').fadeIn();
			}
		});

	}else{
		$('.successmessage, .errormessage').hide();
		$('.mailnotok').fadeIn();
	}
}

