define([
	'underscore',
	'backbone',
	'models/brand'
	], function(_, Backbone, Brand){

		var BrandCollection = Backbone.Collection.extend({
			model: Brand,
			is_current: false,
			initialize: function(option){
				return this;
			},
			set_url : function(url){
				this.url = url;
			},
			fetch : function(){
				// Fetching data here
				var that = this;
				$.ajax({
					url:'brand/'+that.url,
					type:"GET",
					dataType:"json",
					data:{},
					success: function(data, textStatus, jqXHR){
						if(data['status'] === '200'){
							that.reset(data['models']);
						}else{
							that.reset();
						}
						// 
					},
					error: function(jqXHR, textStatus, errorThrown){
						console.log(jqXHR);
						console.log(textStatus);
						console.log(errorThrown);
					}
				});

			},
			addNewBrand: function(newModel){
				this.save(newModel);
			},
			save: function(model){
				// Saving new Model
				console.log(this.url);
				var that = this;
				var url = that.url;
				if (!url){
					url = 0;
				}
				$.ajax({
					url:'brand/'+url,
					type:"POST",
					dataType:"json",
					data:model,
					success: function(data, textStatus, jqXHR){
						if(data['status'] === '200'){
							that.add(data['model']);
						}else{
							that.reset();
						}
					},
					error: function(jqXHR, textStatus, errorThrown){
						console.log(jqXHR);
						console.log(textStatus);
						console.log(errorThrown);
					}
				});

			},
			removeFromServer: function(id_to_remove){
				var that = this;
				$.ajax({
					url:'brand/delete/'+id_to_remove,
					type:"DELETE",
					dataType:"json",
					success: function(data, textStatus, jqXHR){
						if(data['status'] === '200'){
							var model = that.get(id_to_remove);
							that.remove(model);
						}
					},
					error: function(jqXHR, textStatus, errorThrown){
						console.log(jqXHR);
						console.log(textStatus);
						console.log(errorThrown);
					}
				});
			}
		});

		return BrandCollection;
	
})