define([
	'underscore',
	'views/base',
	'views/osms',
	'views/cart-summary',
	'collections/osms',
	'text!../../templates/comparator.html',
	], function(_, BaseView, OsmsView, CartSummaryView, OsmsCollection, comparatorTemplate){

		var ComparatorView = BaseView.extend({
			el: '#comparator',
			template: _.template(comparatorTemplate),
			TRIGGER: 138,
			initialize: function(options){
				this.osms = options.osms || new OsmsCollection([], {'vent': this.vent});
				this.cart = options.cart;
				this.bindTo(this.osms, 'sync change', this.render);
			},
			render: function(){
				// Resetting view
				this.closeSubViews();
				this.$el.empty();

				var active_osm = this.osms.get_active_osm().toJSON();

				// Initializing subviews
				this.$el.append(this.template({'active_osm': active_osm}));
				this.addSubView(new OsmsView({'osms': this.osms, el: this.$el.find('#osms') ,'vent': this.vent}));
				this.addSubView(new CartSummaryView({'cart':this.cart, el: this.$el.find('#mycart'), 'vent': this.vent})); // Cart summary


				// Rendering subviews
				_.each(this.subViews, function(view){
					view.render();
				}, this);

				return this;
			},
			events: {
				'click .cta.commander': 'showExport'
			},
			showExport: function(e){
				this.vent.trigger('modal:show:export');
			}
		});

		return ComparatorView;
})
