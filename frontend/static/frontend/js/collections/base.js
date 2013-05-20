define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseCollection = function (models, options) {
			options || (options = {});
			this.vent = options.vent || {};
			var that = this;

			this.on('sync', function(model, resp, options){
				if ( (typeof that.vent !== 'undefined') && that.vent.hasOwnProperty('trigger') && (typeof resp !== 'undefined') && (typeof resp.carts !== 'undefined')) that.vent.trigger('carts', resp.carts);
				
			});

			this.on('error', function(model, resp, options ){
				if((resp.status === 403) && (typeof model !== 'undefined') && (typeof model.vent !== 'undefined') && (typeof model.vent.trigger !== 'undefined')) model.vent.trigger('user:403');
			})
			
			Backbone.Collection.apply(this, [models, options]);
		};

		_.extend(BaseCollection.prototype, Backbone.Collection.prototype, {});

		BaseCollection.extend = Backbone.Collection.extend;
		
		return BaseCollection;

})