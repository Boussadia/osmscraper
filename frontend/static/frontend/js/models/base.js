define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseModel = function (attributes, options) {
			options || (options = {});
			this.vent = options.vent || {};
			var that = this;

			this.on('sync', function(model, resp, options){
				// console.log(resp.carts);
				// console.log(resp.osm);
				if (typeof that.vent.trigger !== 'undefined') that.vent.trigger('osm', resp.osm);
			});
			
			Backbone.Model.apply(this, [attributes, options]);
		};

		_.extend(BaseModel.prototype, Backbone.Model.prototype, {});

		BaseModel.extend = Backbone.Model.extend;

		return BaseModel;

})