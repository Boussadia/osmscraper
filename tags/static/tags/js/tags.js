$(document).ready(function(){

	$("div.add textarea").autocomplete({
		wordCount:1,
		mode: "outter",
		on: {
			query: function(text,cb){
				var words = [];
				for( var i=0; i<tags.length; i++ ){
					if( tags[i].toLowerCase().indexOf(text.toLowerCase()) == 0 ) words.push(tags[i]);
					if( words.length > 5 ) break;
				}
				cb(words);								
			}
		}
	});

	// Bootstraping app
	$('#main').empty()
	div = get_template_bloc(dalliz_categories, 0, 0)
	$('#main').append(div)


	function get_template_bloc(categories, level, parent){
		var div = $("<div>").addClass("block").attr("id", "level_"+level);
		var ul = $("<ul>");

		for( id in categories){
			var title = categories[id]['name'];
			
			var path_indicator = $('<div>').addClass("path");
			var li = $("<li>").text(title).attr("data-id", id).attr("data-level", level).attr("data-parent", parent);
			li.prepend(path_indicator);

			if($.isEmptyObject(categories[id]['subs'])){
				var button = $("<button>").text("Set").addClass("set_category");
				button.click(function(e){
					var $that = $(this);
					var parent = $that.parent();
					parent.parent().find(".path").removeClass('indicate');
					parent.find('div.path').addClass('indicate');
					var id = parent.attr("data-id");
					var parent_category = parent.attr("data-parent");
					var level = parent.attr("data-level");
					$("#main").addClass("blur");
					$("#pop_over_window").show();
					$(".add").attr("data-id_category",id);
					// Getting data from server
					$.ajax({
						url:'/backend/tags/'+id,
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
							if(data["status"] === 200 ){
								console.log(data['tags'])
								$('#pop_over_window textarea').val(data['tags'])
							}

						},
						error: function(jqXHR, textStatus, errorThrown){
							console.log(jqXHR);
							console.log(textStatus);
							console.log(errorThrown);

							// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
						}
					});

					e.stopPropagation();
				});
				li.append(button);
			}else{

			}
			
			li.click(click_handler);
			ul.append(li);
		}

		div.append(ul);
		return div;
	}

	function click_handler(){
		var $that = $(this);
		var level = $that.attr("data-level");
		var parent = $that.attr("data-parent");
		var id = $that.attr("data-id");
		var sequence = [id];
		var current_level = level-1;
		var current_parent = parent;
		while(current_level>=0){
			var parent_li = $('li[data-level='+current_level+'][data-id='+current_parent+']');
			if (parent_li){
				sequence.unshift(parent_li.attr('data-id'));
			}
			current_level -= 1;
		}
		var categories = dalliz_categories;
		for (i in sequence){
			var s = sequence[i];
			categories = categories[s]['subs'];
		}
		$that.parent().find(".path").removeClass('indicate')
		$that.find('div.path').addClass('indicate');
		div = get_template_bloc(categories, parseInt(level)+1, id);
		if (div.find("li").length>0){
			lvl = parseInt(level);
			while (true){
				var lvl = lvl + 1;
				var lvl_selector = "li[data-level='"+lvl+"']";
				if ($(lvl_selector).length>0){
					$(lvl_selector).parent().parent().remove();
				}else{
					break;
				}
			}
			$("#main").append(div);
		}
	};

	// Handler close button pop over window
	$("#pop_over_window button.close").click(function(){
		$("#main").removeClass("blur");
		$("#pop_over_window").hide();
		$("#pop_over_window .row").remove();
	})

	$(".add button").click(function(){
		var id_category = $(this).parent().attr("data-id_category");
		var tags_string = $('#pop_over_window textarea').val();
		$.ajax({
			url:'/backend/tags/'+id_category+'/'+tags_string,
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
				if (data['status'] === 200) {
					for(i in tags_string.split(" ")){
						if ( !(tags_string.split(" ")[i] in tags)){
							tags.push(tags_string.split(" ")[i]);
						}
					}
				};

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	});

});