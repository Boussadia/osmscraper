define([
	'backbone',
	'analytics'
], function(Backbone, GooglAnalyticsHelper){
	Router = Backbone.Router.extend({
		DEFAULT_URL: '/categorie/cremerie/beurres-et-margarines',
		routes: {
			'': 'index',
			'start': 'index',
			'start/': 'index',
			'categorie/:parentCategoryName/:childCategoryName': 'category',
			'*any':'any'
		},
		initialize: function(options){
			options || (options = {})
			this.vent = options.vent || null;
			GooglAnalyticsHelper.init();
			this.bind('route', this._trackPageview);
			this.vent.on('route:category:force', this.forceCategory, this);
		},
		index: function(){
			var url = this.DEFAULT_URL;
			this.navigate(url, true);
		},
		category: function(parentCategoryName, childCategoryName){
			var url = parentCategoryName+'/'+childCategoryName;
			this.vent.trigger('route:category', {'url': url});
		},
		forceCategory: function(){
			var url;
			url = Backbone.history.getFragment();
			this.vent.trigger('route:category', {'url': url.split('categorie/')[1]});
		},
		any: function(any){
		},
		_trackPageview: function() {
			var url;
			url = Backbone.history.getFragment();
			GooglAnalyticsHelper.track('/'+url);
		}
	});

	return Router;
});