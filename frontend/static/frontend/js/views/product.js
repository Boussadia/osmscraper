define([
	'models/product',
	'views/base',
	'text!../../templates/product.html'
	], function(ProductModel, BaseView, productTemplate){

		var ProductView = BaseView.extend({
			tagName: 'div',
			className: 'product',
			model: ProductModel,
			template: productTemplate,
			initialize: function(options){
				options || (options = {});
				this.product = options.product || new ProductModel({}, {'vent': this.vent});
			},
			render: function(){
				var template = _.template(this.template);
				var data = this.product.toJSON();
				this.$el.append(template(data));
				return this;
			}
		});

		return ProductView;

})