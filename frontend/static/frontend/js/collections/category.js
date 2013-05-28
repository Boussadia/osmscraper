define([
	'collections/base',
	'models/category'
	],function(BaseCollection, CategoryModel){
		
		var CategoryCollection = BaseCollection.extend({
			// Argument that tells if this is the current category that is displayed in main
			current: false,

			model: CategoryModel,
			url: function(){
				return '/api/categories/id/'+this.id+'/subs';
			},
			initialize: function(models, options){
				options || (options = {});
				this.id = options.id || null;
				this.osm = options.osm || '';
				this.current_osm = '';

				this.vent.on('osm:current', function(osm){
					this.current_osm = osm.name;
				}, this);
			},
			parse: function(resp, xhr){
				console.log(resp)
				return resp.subs;
			}

		});

		return CategoryCollection;
})