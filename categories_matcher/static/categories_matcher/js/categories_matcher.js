$(document).ready(function(){

	// Populating select field for adding link between categories
	fill_select('first', dalliz_categories);
	id_category_first = $(".add select#first").find(":selected").val();
	set_sub_categories('first', id_category_first)

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
		if (id_element === "first"){
			fill_select('second', dalliz_categories[id_category]['subs']);
			id_category_second = $(".add select#second").find(":selected").val();
			if (dalliz_categories[id_category]['subs'][id_category_second]){
				fill_select('third', dalliz_categories[id_category]['subs'][id_category_second]['subs'])
			}
		}else if(id_element === "second"){
			id_category_first = $(".add select#first").find(":selected").val();
			fill_select('third', dalliz_categories[id_category_first]['subs'][id_category]['subs'])
		}
	}

	$(".add button").click(function(){
		var id_category = $(this).parent().attr("data-id_category");
		var id_dalliz = $(".add select#third").val();
		var osm = $(this).parent().attr("data-osm");
		console.log(id_category);
		console.log(id_dalliz);
		console.log(osm);
		$.ajax({
			url:'/backend/categories_matcher/add_link',
			type:"POST",
			dataType:"json",
			data:{
				"osm": osm,
				"id_category_final": id_category,
				"id_dalliz_category": id_dalliz
			},
			beforeSend: function(jqXHR, settings){
				console.log(jqXHR);
				console.log(settings);
			},
			success: function(data, textStatus, jqXHR){
				console.log(data);
				console.log(textStatus);
				console.log(jqXHR);
				if(data["status"] === 200 ){
					id_category_first = $(".add select#first").find(":selected").val();
					id_category_second = $(".add select#second").find(":selected").val();
					var category_name = dalliz_categories[id_category_first]['subs'][id_category_second]['subs'][id_dalliz]['display'];
					var div = get_row_link(category_name, id_dalliz, osm, id_category);
					$("#pop_over_window").append(div);

				}

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	});

	// Handler close button pop over window
	$("#pop_over_window button.close").click(function(){
		$("#main").removeClass("blur");
		$("#pop_over_window").hide();
		$("#pop_over_window .row").remove();
	})

	function get_row_link(name_category_dalliz, id_category_dalliz, osm, id_category){
		var div = $("<div>").addClass("row").attr("data-osm", osm).attr("data-id_dalliz", id_category_dalliz).attr("data-id_category",id_category).text(name_category_dalliz);
		var button = $("<button>").text("X");
		button.click(function(){
			$.ajax({
				url:'/backend/categories_matcher/delete_link',
				type:"POST",
				dataType:"json",
				data:{
					"osm": osm,
					"id_category_final": id_category,
					"id_dalliz_category": id_category_dalliz
				},
				success: function(data, textStatus, jqXHR){
					console.log(data);
					console.log(textStatus);
					console.log(jqXHR);
					if(data["status"] === 200 ){
						$(".row[data-id_dalliz='"+id_category_dalliz+"']").remove();

					}

				},
				error: function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);

					// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
				}
			});

		});
		div.append(button);
		return div
	}

	$("#osm li").click(click_handler);


	function get_template_bloc(categories, level, parent, osm){
		var div = $("<div>").addClass("block").attr("id", "level_"+level);
		var ul = $("<ul>");

		for( id in categories){
			var title = categories[id]['name'];
			var is_final = categories[id]['final'];
			var path_indicator = $('<div>').addClass("path");
			var li = $("<li>").text(title).attr("data-osm",osm).attr("data-id", id).attr("data-level", level).attr("data-parent", parent);
			li.prepend(path_indicator);
			

			if(is_final){
				var button = $("<button>").text("Set").addClass("set_category");
				button.click(function(e){
					var $that = $(this);
					var parent = $that.parent();
					parent.parent().find(".path").removeClass('indicate');
					parent.find('div.path').addClass('indicate');
					var osm = parent.attr("data-osm");
					var id = parent.attr("data-id");
					var parent_category = parent.attr("data-parent");
					var level = parent.attr("data-level");
					$("#main").addClass("blur");
					$("#pop_over_window").show();
					$(".add").attr("data-id_category",id);
					$(".add").attr("data-osm",osm);
					$("#pop_over_window button.close").hide();
					// Getting data from server
					$.ajax({
						url:'/backend/categories_matcher/get_links/'+osm+'/'+id,
						type:"GET",
						dataType:"json",
						data:{
						},
						success: function(data, textStatus, jqXHR){
							// console.log(data);
							// console.log(textStatus);
							// console.log(jqXHR);
							for (id_dalliz in data){
								var div = get_row_link(data[id_dalliz], id_dalliz, osm, id);
								$("#pop_over_window").append(div);
							}
							$("#pop_over_window button.close").show();

						},
						error: function(jqXHR, textStatus, errorThrown){
							console.log(jqXHR);
							console.log(textStatus);
							console.log(errorThrown);
							$("#pop_over_window button.close").show();

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
		var osm = $that.attr("data-osm");
		var id = $that.attr("data-id");
		$that.parent().find(".path").removeClass('indicate')
		$that.find('div.path').addClass('indicate');
		$.ajax({
			url:'/backend/categories_matcher/'+osm+'/'+level+'/'+id,
			type:"GET",
			dataType:"json",
			data:{
			},
			success: function(data, textStatus, jqXHR){
				// console.log(data);
				// console.log(textStatus);
				// console.log(jqXHR);
				div = get_template_bloc(data, parseInt(level)+1, id, osm);
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

			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);

				// alert("L'opération ne s'est pas déroulée avec succès, réessayez ultérieurement!");
			}
		});
	};

});