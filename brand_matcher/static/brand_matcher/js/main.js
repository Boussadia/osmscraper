(function(){
	require.config({
		paths: {
			'jquery': 'libs/jquery/jquery',
			'jqueryUi': 'libs/jquery/jqueryui',
			'autocomplete': 'libs/jquery/jquery.autocomplete',
			'underscore': 'libs/underscore/underscore',
			'backbone': 'libs/backbone/backbone',
			'mustache': 'libs/mustache/mustache'
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
			},
			'mustache': {
				exports: 'Mustache'
			}
        }
		
	});

	require([
		// Load our app module and pass it to our definition function
		'app',
		], function(App){
		// The "app" dependency is passed in as "App"
		App.initialize();
		window.App = App;
	});
})();