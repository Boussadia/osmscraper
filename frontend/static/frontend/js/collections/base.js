define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseCollection = function (models, options) {
			options || (options = {});
			this.vent = options.vent || {};
			
			Backbone.Collection.apply(this, [models, options]);
		};

		_.extend(BaseCollection.prototype, Backbone.Collection.prototype, {});

		BaseCollection.extend = Backbone.Collection.extend;
		
		return BaseCollection;

})