define([
	'backbone',
], function(Backbone){
	Router = Backbone.Router.extend({
		initialize: function(option){
			this.vent = option.vent;
			this.on('all', this.storeRoot);
			this.vent.on('route:setSubBrand', this.subBrand, this)
			this.history = [];

			// Routes
			this.route('', "index");
			this.route(/^(.+)$/, "subBrand");

			return this;
		},
		index: function(){
			this.vent.trigger('route:index');
		},
		subBrand: function(e){
			var list = [];
			if(!e){
				var l = this.history.length;
				e = this.history[l-1];
			}
			list = e.split('/');
			_.each(list, function(el){
				if(el === ""){
					list.splice(el,1)
				}
			})
			this.vent.trigger('route:subBrand', list);
		},
		storeRoot: function(){
			this.history.push(Backbone.history.fragment);
		}
	});

	return Router;
});