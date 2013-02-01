(function(){
	// Configuration
	require.config({
		paths: {
			'jquery': 'libs/jquery/jquery',
			'underscore': 'libs/underscore/underscore',
			'backbone': 'libs/backbone/backbone',
			'mustache': 'libs/mustache/mustache',
			'bootstrap': 'libs/bootstrap/bootstrap.min'
		},
		shim: {
			'backbone': {
				deps: ['underscore', 'jquery'],
				exports: 'Backbone'
			},
			'underscore': {
				exports: '_'
			},
			'mustache': {
				exports: 'Mustache'
			},
			'bootstrap': {
				deps: ['jquery'],
				exports: 'Bootstrap'
			}
        }
		
	});

	require([
		// Load our app module and pass it to our definition function
		'app'
		], function(App){
		// Strating app
		var app = new App;
		app.initialize();
		window.app = app;
	});

})();