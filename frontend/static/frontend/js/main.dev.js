(function(){
	require.config({
		urlArgs: "bust=" + (new Date()).getTime(),
		paths: {
			'jquery': 'libs/jquery/jquery',
			'jqueryUi': 'libs/jquery/jqueryui',
			'cookie': 'libs/jquery/jquery.cookie',
			'modernizr': 'libs/modernizr/modernizr.custom.97975',
			'underscore': 'libs/underscore/underscore',
			'backbone': 'libs/backbone/backbone'
		},
		shim: {
			'cookie': {
				deps: ['jquery'],
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
			'modernizr':{
				exports: 'Modernizr'
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