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
				this.suggested = options.suggested;
				this.product = options.product || new ProductModel({}, {'vent': this.vent});

				this.bindTo(this.product, 'change', this.render);
			},
			render: function(){
				this.$el.empty();
				var data = this.product.toJSON();
				data['suggested'] = this.suggested;
				this.$el.append(this.template(data));
				return this;
			},
			events: {
				'click p.minus': 'lessQte',
				'click p.plus': 'moreQte',
				'click .unavailable-mask div:last-child': 'showSubstitution',
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

			},
			showSubstitution: function(e){
				this.vent.trigger('product:recomandation', this.product);
			}
		});

		return MiniProductView;

})