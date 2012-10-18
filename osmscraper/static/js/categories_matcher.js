$(document).ready(function(){

	// Populating select field for adding link between categories
	$(".add").prepend(
		$("<select>")
	);

	$(".add button").click(function(){
		var id_category = $(this).parent().data("id_category");
		var id_dalliz = $(".add select").val();
		var osm = $(this).parent().data("osm");
		$.ajax({
			url:'categories_matcher/add_link',
			type:"POST",
			dataType:"json",
			data:{
				"osm": osm,
				"id_category_final": id_category,
				"id_dalliz_category": id_dalliz
			},
			success: function(data, textStatus, jqXHR){
				console.log(data);
				console.log(textStatus);
				console.log(jqXHR);
				if(data["status"] === 200 ){
					var div = get_row_link(dalliz_categories[id_dalliz], id_dalliz, osm, id_category);
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

	for (id in dalliz_categories){
		name = dalliz_categories[id];
		$(".add select").append(
			$("<option>").text(name).val(id)
		)
	}

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
				url:'categories_matcher/delete_link',
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
			if(id !== "final"){
				var title = categories[id];
				var li = $("<li>").text(title).attr("data-osm",osm).attr("data-id", id).attr("data-level", level).attr("data-parent", parent).attr("data-final", categories["final"]);
				if(categories["final"]){

					var button = $("<button>").text("Set").addClass("set_category");

					button.click(function(e){
						var $that = $(this);
						var parent = $that.parent();
						var osm = parent.data("osm");
						var id = parent.data("id");
						var parent_category = parent.data("parent");
						var level = parent.data("level");
						$("#main").addClass("blur");
						$("#pop_over_window").show();
						$(".add").attr("data-id_category",id);
						$(".add").attr("data-osm",osm);
						// Getting data from server
						$.ajax({
							url:'/categories_matcher/get_links/'+osm+'/'+id,
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
				}
				
				li.click(click_handler);
				ul.append(li);
			}
		}

		div.append(ul);
		return div;
	}

	function click_handler(){
		var $that = $(this);
		var level = $that.data("level");
		var parent = $that.data("parent");
		var osm = $that.data("osm");
		var id = $that.data("id");
		$.ajax({
			url:'/categories_matcher/'+osm+'/'+level+'/'+id,
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