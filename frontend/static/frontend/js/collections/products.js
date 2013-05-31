define([
	'modernizr',
	'collections/base',
	'models/product'
	],
	function(Modernizr, BaseCollection, ProductModel){

		var KEYS = ['top', 'mid', 'end']

		var ProductsCollections = BaseCollection.extend({
			model: ProductModel,
			NUM_INITIAL_PRODUCTS_TO_FETCH: 6,
			TYPE_TO_FETCH: 'products',
			
			// key = 'top' or 'mid' or 'end'
			// this arguments is implemented in order to fetch products acordingly to user needs to look for more products
			index_key: 0,
			url:function(){
				return '/api/categories/id/'+this.id+'/'+this.TYPE_TO_FETCH+'/'+KEYS[this.index_key];
			},
			
			initialize: function(models, options){
				options || (options = {});
				this.TYPE_TO_FETCH = options.type;
				var category_id = options.category_id || null;
				this.id = category_id;


				// If touch device, fetche
				if (Modernizr.touch) this.NUM_INITIAL_PRODUCTS_TO_FETCH = 6;

			},
			parse: function(resp, xhr){
				return resp;
			},
			fetch: function(options){
				options = options ? _.clone(options) : {};
				options.data = {
					'TOP_PRODUCTS_COUNT': this.NUM_INITIAL_PRODUCTS_TO_FETCH
				}
				var more = options.more || false;
				var next_index = this.index_key + 1;

				if (more && next_index<KEYS.length){
					options.remove = false;
					this.index_key = next_index;
				}else if(more && next_index >= KEYS.length){
					return ;
				}else if(!more){
					this.index_key = 0;
				}
				return BaseCollection.prototype.fetch.apply(this, [options]);
			}
		})



		return ProductsCollections;
})