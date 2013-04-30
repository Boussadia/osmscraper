define([
	'underscore',
	'models/product',
	'views/base',
	'text!../../templates/mini-product.html'
	], function(_, ProductModel, BaseView, miniProductTemplate){

		var MiniProductView = BaseView.extend({
			template: _.template(miniProductTemplate),
			className: 'product-recap',
			initialize: function(options){
				options || (options = {});
				this.product = options.product || new ProductModel({}, {'vent': this.vent});

				this.bindTo(this.product, 'change', this.render);
			},
			render: function(){
				this.$el.empty();
				var data = this.product.toJSON();
				this.$el.append(this.template(data));
				return this;
			},
			events: {
				'click p.minus': 'lessQte',
				'click p.plus': 'moreQte'
			},
			moreQte: function(e){
				var quantity = this.product.get('quantity');
				this.product.set('quantity', quantity + 1);
				this.product.save(null, {'cart': true, 'add': 1, 'vent': this.vent});
			},
			lessQte: function(e){
				var quantity = this.product.get('quantity');
				if (quantity-1>=0){
					this.product.set('quantity', quantity - 1);
					this.product.save(null, {'cart': true, 'remove': 1, 'vent': this.vent});
				}

			}
		});

		return MiniProductView;

})