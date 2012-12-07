define([
	'jquery',
	'underscore',
	'backbone',
	'router', // Request router.js
], function($, _ , Backbone, Router){
	var initialize = function(){
		// Pass in our Router module and call it's initialize function
		var router = new Router();
		Backbone.history.start({ pushState: true, root: "/brand/ooshop/" });
	}

	return {
		initialize: initialize
	};
});