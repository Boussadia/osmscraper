define([
	'backbone'
	], function(Backbone){
		var Category = Backbone.Model.extend({
			default:{
				'name': 'category',
				'parent_category': null,
				'position': 0,
				'url': null,
			},
			initialize: function(){

			},
			savePosition: function(position){
				this.set('position', position)
				var that = this;
				$.ajax({
					url: '/backend/categorie/id/'+that.get('id')+'/position/'+that.get('position')+'/',
					type: 'POST',
					data: {},
					dataType: 'JSON',
					success: function(a, b, c){

					}
				})
			}
		});
		return Category;

})