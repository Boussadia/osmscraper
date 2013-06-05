define([
	'underscore',
	'models/product',
	'views/base',
	'text!../../templates/product.html'
	], function(_, ProductModel, BaseView, productTemplate){

		var ProductView = BaseView.extend({
			// maximum length of product name,
			MAX_NAME_LENGTH: 40,
			tagName: 'div',
			className: 'product',
			model: ProductModel,
			template: _.template(productTemplate),
			initialize: function(options){
				options || (options = {});
				this.product = options.product || new ProductModel({}, {'vent': this.vent});

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
			addToCart: function(){
				var quantity = this.product.get('quantity_in_cart');
				this.product.set('quantity_in_cart', quantity + 1);
				this.product.save(null, {'cart': true, 'add': 1, 'vent': this.vent});
			},
			removeFromCart: function(){
				var quantity = this.product.get('quantity_in_cart');
				if (quantity-1>=0){
					this.product.set('quantity_in_cart', quantity - 1);
					this.product.save(null, {'cart': true, 'remove': 1, 'vent': this.vent});
					this.vent.trigger('product:quantity:set', {
						'reference': this.product.get('reference'),
						'quantity': this.product.get('quantity_in_cart')
					})
				}

			}

		});

		return ProductView;

})