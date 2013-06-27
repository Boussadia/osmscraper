$(document).ready(function(){
	$('#email').keypress(function(e){
		var code = e.charCode;
		if (code === 13) {
			e.preventDefault();
			$('#ok').trigger('click');
		};
	})
	$('#ok').click(function(e){
		e.preventDefault();
		var mail = $('#email').val();
		send_mail_prospect(mail);
	});



	$('#sign-in-button').click(function(e){
		e.preventDefault();
		var name = $('#sign-in .form-container input[type=email]').val();
		var pass = $('#sign-in .form-container input[type=password]').val();
		login(name, pass)
	});

	$('#sign-in .form-container input').keypress(function(e){
		var code = e.charCode;
		if (code === 13) {
			e.preventDefault();
			$('#sign-in-button').trigger('click');
		};
	})
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
				$('.show').hide().removeClass('show');
				$('.errormessage').fadeIn();
				$('.errormessage').addClass('show');
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(jqXHR);
				// console.log(textStatus);
				$('.show').hide().removeClass('show');
				$('#successmessage').fadeIn();
				$('#successmessage').addClass('show');
			}
		});

	}else{
		$('.show').hide().removeClass('show');
		$('.mailnotok').fadeIn();
		$('.mailnotok').addClass('show');
	}
}

function login(name, pass){

	$.ajax({
		url:'/api/auth/login',
		type:"POST",
		dataType:"json",
		data:{
			"username" : name,
			"password" : pass
		},
		error: function(jqXHR, textStatus, errorThrown){
			
			// $('#successmessage, .errormessage').hide();
			// $('.errormessage').fadeIn();
		},
		success: function(data, textStatus, jqXHR){
			// console.log($('#sign-in form'));
			$('#sign-in form').submit();
			// window.location = '/comparateur/start/'
		}
	});
}


// Specific methods for csrf control
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || 
			(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e relative.
			!(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			var csrftoken = $.cookie('csrftoken');
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			// Using the CSRFToken value acquired earlier
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

