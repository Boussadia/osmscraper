define([
	'backbone',
	'analytics'
], function(Backbone, GooglAnalyticsHelper){
	Router = Backbone.Router.extend({
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
		},
		index: function(){
			var url = '/categorie/epicerie-sucree/cafes-et-chicorees';
			this.navigate(url, true);
		},
		category: function(parentCategoryName, childCategoryName){
			var url = parentCategoryName+'/'+childCategoryName;
			this.vent.trigger('route:category', {'url': url});
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