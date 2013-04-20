define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'views/menu',
	'views/main'
], function($, _ , Backbone, Router, MenuView, MainView){

	function MasterCoursesApp(){
		// Mustache style templatating
		_.templateSettings = {
			interpolate : /\{\{(.+?)\}\}/g,
		};

		// Global Scope
		this.Views = {};
		this.Collections = {};
		this.Models = {};

		// Global event manager
		this.Vent = _.extend({}, Backbone.Events);

		// Settings listeners
		this.Vent.on('route:category', this.category, this);
		// this.Vent.on('route:product', this.product, this);
	}

	/*******************************************************************************************************************************************
	*
	*											METHOD TRIGGERED BY ROUTE EVENTS
	*	
	*******************************************************************************************************************************************/

	MasterCoursesApp.prototype.category = function(options){
		options || (options = {});
		var category_id = options.id || null;
		if(category_id){
			console.log(category_id);
		}
	}

	// Method to call in order to start application
	MasterCoursesApp.prototype.initialize = function(){
		// Menu
		this.Views.menu = new MenuView({'vent': this.Vent});
		var that = this;
		// Callback function needed in order to wait for the menu to be built
		this.Views.menu.build(function(){
			// Router module
			var router = new Router({'vent': that.Vent});
			Backbone.history.start({ pushState: true, root:"/dev"});

			// Use absolute URLs  to navigate to anything not in your Router.

			// Only need this for pushState enabled browsers
			if (Backbone.history && Backbone.history._hasPushState) {

				// Use delegation to avoid initial DOM selection and allow all matching elements to bubble
				$(document).delegate("a:not(.no-hijax)", "click", function(evt) {
					// Get the anchor href and protcol
					var href = $(this).attr("href");
					var protocol = this.protocol + "//";
					// Ensure the protocol is not part of URL, meaning its relative.
					// Stop the event bubbling to ensure the link will not cause a page refresh.
					if (href.slice(protocol.length) !== protocol) {
						evt.preventDefault();

						// Note by using Backbone.history.navigate, router events will not be
						// triggered.  If this is a problem, change this to navigate on your
						// router.
						router.navigate(href, true);
					}
				});
			}

		});

		// Main View
		this.Views.main = new MainView({'vent': this.Vent});

	}

	return MasterCoursesApp;
});