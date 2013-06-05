define([
	'modernizr',
	'collections/base',
	'models/product'
	],
	function(Modernizr, BaseCollection, ProductModel){

		var ProductsCollections = BaseCollection.extend({
			model: ProductModel,
			PRODUCTS_PER_PAGE: 5,
			TYPE_TO_FETCH: 'products',
			
			// key = 'top' or 'mid' or 'end'
			// this arguments is implemented in order to fetch products acordingly to user needs to look for more products
			index_key: 0,
			url:function(){
				return '/api/categories/id/'+this.id+'/'+this.TYPE_TO_FETCH;
			},
			
			initialize: function(models, options){
				options || (options = {});
				this.TYPE_TO_FETCH = options.type;
				var category_id = options.category_id || null;
				this.id = category_id;
				this.fetched_pages = [];
				this.page = 1;
				this.max_pages = 2;
				this.next =  null;
				this.previous =  null;
				this.brands = [];

				// If touch device, fetche
				if (Modernizr.touch) this.PRODUCTS_PER_PAGE = 6;

			},
			parse: function(resp, xhr){
				this.count = resp.count;
				this.max_pages = Math.ceil(this.count/this.PRODUCTS_PER_PAGE);
				this.next = resp.next;
				this.previous = resp.previous;
				return resp.results;
			},
			fetch: function(options){
				options = options ? _.clone(options) : {};

				var more = options.more || false;
				var reset = options.reset || false;
				var callback = options.callback || null;
				var that = this;
				var brands = options.brands || this.brands;
				this.brands = brands;

				if (more){
					options.remove = false;
					var next = this.next;
					if (next) this.page = (this.page < this.next ? this.page + 1 : next);
				}

				if(reset){
					this.fetched_pages = [];
					this.page = 1;
					this.max_pages = 2;
					this.next =  null;
					this.previous =  null;
				}


				var page_to_fetch = this.page;

				if (this.fetched_pages.indexOf(page_to_fetch)>=0) return null;

				options.data = {
					'PRODUCTS_PER_PAGE': this.PRODUCTS_PER_PAGE,
					'page': this.page,
					'brands': brands
				}

				options.success = function(collection, response, option){
					that.vent.trigger('request:products:quantity', {'products': collection.toJSON()});
					that.fetched_pages.push(page_to_fetch);
					if (callback) callback();
				}
				return BaseCollection.prototype.fetch.apply(this, [options]);
			}
		})



		return ProductsCollections;
})