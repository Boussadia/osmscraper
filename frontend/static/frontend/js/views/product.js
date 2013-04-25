define([
	'models/product',
	'views/base',
	'text!../../templates/product.html'
	], function(ProductModel, BaseView, productTemplate){

		var ProductView = BaseView.extend({
			// maximum length of product name,
			MAX_NAME_LENGTH: 142,
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
				if (data.name.length > this.MAX_NAME_LENGTH){
					console.log(data.name.length);
					data.name = data.name.substring(0, this.MAX_NAME_LENGTH-3)+'...';
				}
				this.$el.append(template(data));
				return this;
			}
		});

		return ProductView;

})