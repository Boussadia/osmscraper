define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'views/menu',
], function($, _ , Backbone, Router, MenuView){
	var initialize = function(){
		// Mustache style templatating
		_.templateSettings = {
			interpolate : /\{\{(.+?)\}\}/g
		};

		// Global event manager
		this.Vent = _.extend({}, Backbone.Events);

		// Global Scope
		this.Views = {};
		this.Collections = {};
		this.Models = {};

		// Menu
		this.Views.menu = new MenuView({'vent': this.Vent});

		// Router module
		var router = new Router({'vent': this.Vent});
		Backbone.history.start({ pushState: true, root:"/dev"});
	}

	return {
		initialize: initialize
	};
});