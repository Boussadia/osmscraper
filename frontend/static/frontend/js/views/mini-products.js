define([
	'collections/miniproducts',
	'views/base',
	'views/mini-product'
	], function(MiniProductsCollections, BaseView, MiniProductView){

		var MiniProductsView = BaseView.extend({
			className: 'products-recap',
			initialize: function(options){
				this.products = options.products || new MiniProductsCollections([], {'vent': this.vent});

			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				this.products.each(function(product){
					var view = new MiniProductView({'product': product, 'vent': this.vent});
					this.addSubView(view);
				}, this);

				_.each(this.subViews, function(view){
					this.$el.append(view.render().el);
				}, this);

				return this;
			}
		});

		return MiniProductsView;
})