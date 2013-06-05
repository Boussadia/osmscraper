define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseModel = function (attributes, options) {
			options || (options = {});
			this.vent = options.vent || {};
			var that = this;

			this.on('sync', function(model, resp, options){
				if ( (typeof model !== 'undefined') && (typeof model.vent !== 'undefined') && model.vent.hasOwnProperty('trigger') && (typeof resp !== 'undefined') && (typeof resp.carts !== 'undefined')) model.vent.trigger('carts', resp.carts);
			});

			this.on('error', function(model, resp, options ){
				if((resp.status === 403) && (typeof model !== 'undefined') && (typeof model.vent !== 'undefined') && (typeof model.vent.trigger !== 'undefined')) model.vent.trigger('user:403');
			});
			
			Backbone.Model.apply(this, [attributes, options]);
		};

		_.extend(BaseModel.prototype, Backbone.Model.prototype, {});

		BaseModel.extend = Backbone.Model.extend;

		return BaseModel;

})