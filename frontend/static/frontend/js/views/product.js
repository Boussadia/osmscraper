define([
	'models/product',
	'views/base',
	'text!../../templates/product.html'
	], function(ProductModel, BaseView, productTemplate){

		var ProductView = BaseView.extend({
			tagName: 'li',
			classeName: 'product',
			model: ProductModel,
			template: productTemplate,
			initialize: function(options){
				options || (options = {});
				this.product = options.product || new ProductModel({'vent': this.vent});
			},
			render: function(){
				this.$el.empty();
				var template = _.template(this.template);
				var data = this.product.toJSON();
				this.$el.append(template(data));
				return this;
			}
		});

		return ProductView;

})