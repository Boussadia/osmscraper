define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'collections/osms',
	'models/osm',
	'models/cart',
	'models/user',
	'views/menu',
	'views/main',
	'views/comparator',
	'views/cart',
	'views/login',
	'views/userbar',
	'views/switch',
	'cookie'
], function($,_ , Backbone, Router, OsmsCollections, OsmModel, CartModel, UserModel, MenuView, MainView, ComparatorView, CartView, LoginView, UserBarView, SwitchView){

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
			if(method === 'create' || method === 'update' || method === 'patch'){
				options.attrs || (options.attrs = {});
				_.extend(options.attrs, that.data);
				// Removing location if null (causes 500 error from server)
				if(!options.attrs.osm_location) delete options.attrs.osm_location;
			}else{
				options.data || (options.data = {});
				_.extend(options.data, that.data);
				// Removing location if null (causes 500 error from server)
				if(!options.data.osm_location) delete options.data.osm_location;
			}

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

		// Login view
		this.Views.login = new LoginView({'vent': this.Vent});

		// User
		this.Models.user = new UserModel({}, {'vent': this.Vent});
		this.Models.user.fetch(); // Getting user details from server
		this.Views.userbar = new UserBarView({'user': this.Models.user, 'vent': this.Vent});
		this.Views.userbar.render();

		// Comparator, rendering comparator after fetching menu
		this.Collections.osms = new OsmsCollections([], {'vent': this.Vent});
		this.Collections.osms.add([{'name': 'auchan'}, {'name': 'monoprix'}, {'name': 'ooshop'}], {'vent': this.Vent});

		// Cart
		this.Models.cart = new CartModel({}, {'vent': this.Vent});
		this.Views.cart = new CartView({'cart': this.Models.cart, 'vent': this.Vent});
		this.Models.cart.fetch();

		// Switch
		this.Views.switch = new SwitchView({'osms': this.Collections.osms, 'vent': this.Vent});

		var that = this;

		// Callback function needed in order to wait for the menu to be built
		this.Views.menu.build(function(){
			bootstrap(that);
			// Here rendering comprator (for interface construction coherence)
			that.Views.comparator = new ComparatorView({'osms':that.Collections.osms , 'vent': that.Vent});
			// that.Views.comparator.render();
		});

		// Main View
		this.Views.main = new MainView({'vent': this.Vent});

	}

	// Application bootstraping
	function bootstrap(application){
			// Router module
			var router = new Router({'vent': application.Vent});
			application.Router = router;
			Backbone.history.start({ pushState: true, root:"/comparateur"});

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
					if (protocol !== 'javascript://' && href && href.slice(protocol.length) !== protocol) {
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
				application.Vent.trigger('window:scroll');
			})

		}

	// Specific methods for csrf control
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	function sameOrigin(url) {
		// test that a given url is a same-origin URL
		// url could be relative or scheme relative or absolute
		var host = document.location.host; // host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || 
				(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
				// or any other URL that isn't scheme relative or absolute i.e relative.
				!(/^(\/\/|http:|https:).*/.test(url));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				var csrftoken = $.cookie('csrftoken');
				// Send the token to same-origin, relative URLs only.
				// Send the token only if the method warrants CSRF protection
				// Using the CSRFToken value acquired earlier
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	return MasterCoursesApp;
});