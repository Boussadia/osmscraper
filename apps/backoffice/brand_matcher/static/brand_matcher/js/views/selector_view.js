define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'models/choices',
	'models/osm_brand',
	'jqueryUi'
], function($,_, Backbone, Mustache, Choices, osm_brand){
	var SelectorView = Backbone.View.extend({
		el: $('section#content'),
		router: null,
		render: function(){
			this.set_proper_data();
			var template = $('#template').text();
			var out = Mustache.render(template, template_value);
			this.$el.html(out);
			var suggested = {};
			var that = this;

			$('input#autocomplete').autocomplete({
				autoFocus: true,
				source: "/backend/matcher/brand/autocomplete/",
				select: function( event, ui ) {
					suggested = ui['item'];
				}
			});

			$('#more button').click(function(){
				if (Object.keys(suggested).length > 0){
					template_value['dalliz_brands'].push(suggested);
					that.render().$el.find('button[data-id='+suggested['id']+']')
										.click();
				}
			})
			// Keybord listener on previous and next
			$('html').keyup(function(e){
				if(e.keyCode === 39){
					// Next
					$('#btn-next').click();
				}else if(e.keyCode === 37){
					// Previous
					$('#btn-previous').click();
				}
			})
			return this
		},
		set_proper_data: function(){
			this.choices = new Choices(template_value['dalliz_brands']);
			this.osm_brand = new osm_brand(template_value['osm_brand']);
		},
		initialize: function(){
			this.set_proper_data();
			return this;
		},
		events: {
			"click #btn-cancel": "cancel_match",
			"click #btn-next": "fetch",
			"click #btn-previous": "fetch",
			"click .btn-selection": "set_match",

		},
		cancel_match: function(e){
			this.remove_UI_match(); // Removing UI indicator
			this.osm_brand.cancel_match(); // Removing in database
		},
		set_match: function(e){
			// this.remove_UI_match();// Removing UI indicator

			// Processing data
			var id = $(e.target).data(id);
			var choice = this.choices.get(id)
			choice.set_match(this.osm_brand.get('id'), this.osm_brand.get('osm'));

			// Removing Ui indicator
			$('.info').removeClass('info');
			// Setting UI indicator
			$(e.target).parent().parent().addClass('info');
		},
		fetch: function(e){
			var id = $(e.target).data('id');
			this.router.navigate('/backend/matcher/'+this.osm_brand.get('osm')+'/brand/'+id+'/', {trigger: true});
		},
		remove_UI_match: function(){
			$('.info').removeClass('info')
		},
		set_router: function(router){
			this.router = router;
		}

	})

	return SelectorView;
});