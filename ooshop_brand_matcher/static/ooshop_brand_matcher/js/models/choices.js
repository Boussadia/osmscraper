define([
	'jquery',
	'underscore',
	'backbone',
	'models/match'
], function($,_, Backbone, Match){
	var Choices = Backbone.Collection.extend({
		model: Match,
		initialize: function(){
			
		}
	})

	return Choices

});