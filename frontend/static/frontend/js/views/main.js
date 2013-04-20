define([
	'jquery',
	'underscore',
	'backbone',
	'views/base'
], function($, _, Backbone, BaseView){

	var MainView = BaseView.extend({
		el: 'section#main',
		initialize: function(){
		}
	});


	return MainView;
})