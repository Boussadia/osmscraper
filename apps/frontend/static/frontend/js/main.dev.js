(function(){
	require.config({
		paths: {
			'jquery': 'libs/jquery/jquery',
			'jqueryUi': 'libs/jquery/jqueryui',
			'dropit': 'libs/jquery/dropit',
			'cookie': 'libs/jquery/jquery.cookie',
			'modernizr': 'libs/modernizr/modernizr.custom',
			'underscore': 'libs/underscore/underscore',
			'backbone': 'libs/backbone/backbone',
			'foundation': 'libs/foundation/foundation.min',
			'analytics': 'libs/google/analytics',
			'typeahead': 'libs/typeahead.js/typeahead'
		},
		shim: {
			'cookie': {
				deps: ['jquery'],
			},
			'jqueryUi': {
				deps: ['jquery'],
			},
			'dropit': {
				deps: ['jquery'],
			},
			'backbone': {
				deps: ['underscore', 'jquery'],
				exports: 'Backbone'
			},
			'underscore': {
				exports: '_'
			},
			'modernizr': {
				exports: 'Modernizr'
			},
			'foundation': {
				deps: ['jquery']
			},
			'typeahead': {
				deps: ['jquery']
			}
		},
		
	});

	require([
		// Load our app module and pass it to our definition function
		'app',
		], function(MasterCoursesApp){
		// The "app" dependency is passed in as "App"
		var App = new MasterCoursesApp();
		App.initialize();
		window.App = App;
	});
})();