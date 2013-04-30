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
				var data = this.product.toJSON();
				this.$el.append(this.template(data));
				return this;
			}
		});

		return MiniProductView;

})