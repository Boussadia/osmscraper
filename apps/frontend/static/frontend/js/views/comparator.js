define([
	'underscore',
	'views/base',
	'views/osms',
	'views/switch-area',
	'views/order',
	'views/cart-summary',
	'collections/osms',
	'text!../../templates/comparator.html'
	], function(_, BaseView, OsmsView, SwitchAreaView, OrderView, CartSummaryView, OsmsCollection, comparatorTemplate){

		var ComparatorView = BaseView.extend({
			el: '#comparator',
			template: _.template(comparatorTemplate),
			TRIGGER: 138,
			initialize: function(options){
				this.osms = options.osms || new OsmsCollection([], {'vent': this.vent});
				this.cart = options.cart;
				this.bindTo(this.osms, 'sync', this.render);
			},
			render: function(){
				// Resetting view
				this.closeSubViews();
				this.$el.empty();

				// Initializing subviews
				this.$el.append(this.template({}));
				this.addSubView(new OsmsView({'osms': this.osms, el: this.$el.find('#osms') ,'vent': this.vent}));
				this.addSubView(new SwitchAreaView({'osms': this.osms, el: this.$el.find('#switch-area') ,'vent': this.vent}));
				this.addSubView(new OrderView({'osms': this.osms, el: this.$el.find('#active-osm') ,'vent': this.vent}));
				this.addSubView(new CartSummaryView({'cart':this.cart, el: this.$el.find('#mycart'), 'vent': this.vent})); // Cart summary


				// Rendering subviews
				_.each(this.subViews, function(view){
					view.render();
				}, this);

				return this;
			}
		});

		return ComparatorView;
})
