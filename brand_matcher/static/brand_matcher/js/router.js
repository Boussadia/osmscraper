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

			// Regex route : /brand/osm/:id
			this.route(/^backend\/matcher\/(\w+)\/brand\/(\d+)\/?$/, 'selector');
			return this;
		},
		selector: function(osm, id){
			var router = this;
			$.ajax({
				url: '/backend/matcher/'+osm+'/brand/'+id+'/',
				type:"GET",
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