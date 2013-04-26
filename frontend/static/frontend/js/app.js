define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'collections/osms',
	'models/osm',
	'views/menu',
	'views/main',
	'views/comparator'
], function($, _ , Backbone, Router, OsmsCollections, OsmModel, MenuView, MainView, ComparatorView){

	function MasterCoursesApp(){
		// Global Scope
		this.Views = {};
		this.Collections = {};
		this.Models = {};

		// Global event manager
		this.Vent = _.extend({}, Backbone.Events);


		// Data sent to server to control osm
		this.data = {
			'osm_name': 'monoprix',
			'osm_type': 'shipping',
			'osm_location': null
		}
		var that = this;

		// Overriding base Backbone sync method
		Backbone.originalSync = Backbone.sync; // Saving reference of original sunc method
		Backbone.sync = function(method, model, options){
			options || (options = {});
			options.data || (options.data = {});
			_.extend(options.data, that.data);

			// Removing location if null (causes 500 error from server)
			if(!options.data.osm_location) delete options.data.osm_location;

			return Backbone.originalSync(method, model, options);
		}

		// Settings listeners
		this.Vent.on('route:category', this.category, this);
		// this.Vent.on('route:product', this.product, this);
		this.Vent.on('osm', function(osm){
			// Settings values of osm
			that.data.osm_location = osm.location;
			that.data.osm_name = osm.name;
			that.data.osm_type = osm.type;
		}, this);

		// this.Vent.on('carts', function(carts){
		// 	console.log(carts);
		// })
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
			this.Views.main.addCategory(category_id);
		}
	}

	// Method to call in order to start application
	MasterCoursesApp.prototype.initialize = function(){
		// Menu
		this.Views.menu = new MenuView({'vent': this.Vent});
		// Comparator
		this.Collections.osms = new OsmsCollections([], {'vent': this.Vent});
		this.Collections.osms.add([{'name': 'auchan'}, {'name': 'monoprix'}, {'name': 'ooshop'}], {'vent': this.Vent});


		this.Views.comparator = new ComparatorView({'osms':this.Collections.osms , 'vent': this.Vent});
		// this.Views.comparator.render();

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

			// Setting listner of scroll events on window
			$(window).scroll(function(event){
				that.Vent.trigger('window:scroll');
			})

		});

		// Main View
		this.Views.main = new MainView({'vent': this.Vent});

	}

	return MasterCoursesApp;
});