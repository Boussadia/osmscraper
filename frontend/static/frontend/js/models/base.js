define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseModel = function (attributes, options) {
			options || (options = {});
			this.vent = options.vent || {};
			var that = this;

			this.on('sync', function(model, resp, options){
				if (typeof that.vent.trigger !== 'undefined') that.vent.trigger('osm', resp.osm);
				if (typeof that.vent.trigger !== 'undefined') that.vent.trigger('carts', resp.carts);
			});
			
			Backbone.Model.apply(this, [attributes, options]);
		};

		_.extend(BaseModel.prototype, Backbone.Model.prototype, {});

		BaseModel.extend = Backbone.Model.extend;

		return BaseModel;

})