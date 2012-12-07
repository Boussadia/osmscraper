define([
	'jquery',
	'underscore',
	'backbone',
	'views/selector_view'
], function($, _, Backbone, SelectorView){
	Router = Backbone.Router.extend({
		routes: {},
		initialize: function(){
			// View
			this.selector_view = new SelectorView();
			this.selector_view.set_router(this);

			// Regex route : /brand/ooshop/:id
			this.route(/^brand\/ooshop\/(\d+)\/?$/, 'selector');
			return this;
		},
		selector: function(id){
			var router = this;
			$.ajax({
				url: '/brand/ooshop/'+id+'/',
				type:"POST",
				dataType:"json",
				data:{},
				success: function(data, textStatus, jqXHR){
					var template = data['template'];
					template_value = $.parseJSON(data['template_value']);
					$('#template').text(template);
					router.selector_view.render();
				},
				error: function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);
				}
			});
		}
	});

	return Router;
});