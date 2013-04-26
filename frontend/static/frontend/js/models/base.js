define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseModel = function (attributes, options) {
			options || (options = {});
			this.vent = options.vent || {};
			var that = this;

			this.on('all', function(model, resp, options){
				if ( (typeof model !== 'undefined') && (typeof model.vent !== 'undefined') && model.vent.hasOwnProperty('trigger') && resp !== undefined && resp.osm !== undefined) model.vent.trigger('osm', resp.osm);
				if ( (typeof model !== 'undefined') && (typeof model.vent !== 'undefined') && model.vent.hasOwnProperty('trigger') && resp !== undefined && resp.carts !== undefined) model.vent.trigger('carts', resp.carts);
			});
			
			Backbone.Model.apply(this, [attributes, options]);
		};

		_.extend(BaseModel.prototype, Backbone.Model.prototype, {});

		BaseModel.extend = Backbone.Model.extend;

		return BaseModel;

})