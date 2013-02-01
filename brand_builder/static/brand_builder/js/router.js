define([
	'backbone',
], function(Backbone){
	Router = Backbone.Router.extend({
		initialize: function(option){
			this.vent = option.vent;
			this.on('all', this.storeRoot);
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