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
		// Global Scope
		this.Views = {};
		this.Collections = {};
		this.Models = {};

		// Menu
		this.Views.menu = new MenuView();

		// Router module
		var router = new Router();
		Backbone.history.start({ pushState: true, root:"/dev"});
	}

	return {
		initialize: initialize
	};
});