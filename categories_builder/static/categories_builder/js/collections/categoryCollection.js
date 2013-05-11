define([
	'underscore',
	'backbone',
	'models/category'
	], function(_, Backbone, Category){

		var CategoryCollection = Backbone.Collection.extend({
			model: Category,
			is_current: false,
			initialize: function(option){
				return this;
			},
			set_url : function(url){
				this.url = url;
			},
			set_parent_url : function(parent_url){
				this.parent_url = parent_url;
			},
			fetch : function(){
				// Fetching data here
				var that = this;
				var url = that.url;
				if(that.parent_url) url = that.parent_url+'/'+url;
				$.ajax({
					url:url,
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
			addNewCategory: function(newModel){
				this.save(newModel);
			},
			save: function(model){
				// Saving new Model
				var that = this;
				var url = that.url;
				if(that.parent_url) url = that.parent_url+'/'+url;
				$.ajax({
					url:url,
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
					url:'delete/'+id_to_remove,
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

		return CategoryCollection;
	
})
