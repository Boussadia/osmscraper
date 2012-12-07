define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'models/choices',
	'models/ooshop_brand'
], function($,_, Backbone, Mustache, Choices, Ooshop_brand){
	var SelectorView = Backbone.View.extend({
		el: $('section#content'),
		router: null,
		render: function(){
			this.set_proper_data();
			var template = $('#template').text();
			var out = Mustache.render(template, template_value);
			this.$el.html(out);
		},
		set_proper_data: function(){
			this.choices = new Choices(template_value['dalliz_brands']);
			this.ooshop_brand = new Ooshop_brand(template_value['ooshop_brand']);
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
			this.ooshop_brand.cancel_match(); // Removing in database
		},
		set_match: function(e){
			this.remove_UI_match();// Removing UI indicator

			// Processing data
			var id = $(e.target).data(id);
			var choice = this.choices.get(id)
			choice.set_match(this.ooshop_brand.get('id'));

			// Setting UI indicator
			$(e.target).parent().parent().addClass('info');
		},
		fetch: function(e){
			var id = $(e.target).data('id');
			this.router.navigate('/brand/ooshop/'+id+'/', {trigger: true});
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