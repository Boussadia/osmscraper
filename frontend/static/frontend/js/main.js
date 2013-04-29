(function(){
	require.config({
		paths: {
			'jquery': 'libs/jquery/jquery',
			'jqueryUi': 'libs/jquery/jqueryui',
			'autocomplete': 'libs/jquery/jquery.autocomplete',
			'underscore': 'libs/underscore/underscore',
			'backbone': 'libs/backbone/backbone'
		},
		shim: {
			'autocomplete': {
				deps: ['jqueryUi', 'jquery'],
			},
			'jqueryUi': {
				deps: ['jquery'],
			},
			'backbone': {
				deps: ['underscore', 'jquery'],
				exports: 'Backbone'
			},
			'underscore': {
				exports: '_'
			}
        }
		
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