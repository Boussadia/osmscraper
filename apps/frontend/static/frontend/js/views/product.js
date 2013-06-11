define([
	'underscore',
	'models/product',
	'views/base',
	'text!../../templates/product.html'
	], function(_, ProductModel, BaseView, productTemplate){

		var ProductView = BaseView.extend({
			// maximum length of product name,
			MAX_NAME_LENGTH: 40,
			BUFFER_INTERVAL_TIME: 1000, // time in milliseconds
			tagName: 'div',
			className: 'product',
			model: ProductModel,
			template: _.template(productTemplate),
			initialize: function(options){
				options || (options = {});
				this.product = options.product || new ProductModel({}, {'vent': this.vent});
				this.buffered_quantity = 0;
				this.last_update = (new Date().getTime());

				this.bindTo(this.product, 'change', this.render);
			},
			render: function(){
				// Only render if associated product was fetched from server
				this.$el.empty();
				var data = this.product.toJSON();
				if (data.name.length > this.MAX_NAME_LENGTH){
					data.name = data.name.substring(0, this.MAX_NAME_LENGTH-3)+'...';
				}
				this.$el.append(this.template(data));

				return this;
			},
			events: {
				'click a.add-cart': 'addToCart',
				'click a.plus': 'addToCart',
				'click a.minus': 'removeFromCart',
			},
			addToCart: function(e, delayed, options){
				options || (options = {});
				var that = this;

				if (!delayed){
					var now = (new Date().getTime());
					var diff = now - this.last_update;
					this.buffered_quantity = this.buffered_quantity + 1;
					var quantity = options.quantity || this.product.get('quantity_in_cart');
					quantity = quantity + 1;
					this.product.set('quantity_in_cart', quantity);
				}

				if (diff<=this.BUFFER_INTERVAL_TIME*10){
					setTimeout(function(){
						that.addToCart(null, true);
					}, this.BUFFER_INTERVAL_TIME);
				}else{
					_.extend(options, {'cart': true, 'quantity': that.buffered_quantity, 'vent': that.vent});
					that.product.save(null, options);
					that.buffered_quantity = 0;
					that.last_update = now;

				}
			},
			removeFromCart: function(e, delayed, options){
				options || (options = {});
				var that = this;

				if (!delayed){
					var now = (new Date().getTime());
					var diff = now - this.last_update;
					this.buffered_quantity = this.buffered_quantity + 1;
					var quantity = options.quantity || this.product.get('quantity_in_cart');
					quantity = quantity - 1;
					if (quantity>=0){
						this.product.set('quantity_in_cart', quantity);
					}else{
						this.buffered_quantity = this.buffered_quantity - 1;
					}
				}

				if (diff<=this.BUFFER_INTERVAL_TIME*10){
					setTimeout(function(){
						that.removeFromCart(null, true);
					}, this.BUFFER_INTERVAL_TIME);
				}else{
					_.extend(options, {'cart': true, 'remove': true,'quantity': that.buffered_quantity, 'vent': that.vent});
					that.product.save(null, options)
					that.buffered_quantity = 0;
					that.last_update = now;
				}

			}

		});

		return ProductView;

})