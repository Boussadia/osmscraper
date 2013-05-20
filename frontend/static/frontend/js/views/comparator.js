define([
	'underscore',
	'views/base',
	'views/osms',
	'views/switch-area',
	'views/order',
	'collections/osms',
	'text!../../templates/comparator.html'
	], function(_, BaseView, OsmsView, SwitchAreaView, OrderView, OsmsCollection, comparatorTemplate){

		var ComparatorView = BaseView.extend({
			el: '#comparator',
			template: _.template(comparatorTemplate),
			TRIGGER: 138,
			initialize: function(options){
				this.osms = options.osms || new OsmsCollection([], {'vent': this.vent});

				// Setting active osm
				this.active_osm = {
					price: 0,
					name: 'monoprix',
					minimum: 70
				}
				var active_osm = _.find(this.osms.toJSON(), function(osm){
					return osm.active;
				});
				this.active_osm = active_osm || this.active_osm;

				// Listening to events
				this.vent.on('carts', function(carts){
					
					// Getting cart with minimum cart price
					var min = _.min(carts, function(cart){
						return cart.price
					});

					// Setting price to save
					try{
						this.data = {
							price_to_save: - (this.active_osm.price-min.price),
						}
					}catch(e){}

					this.render();
				},this);

				this.vent.on('osm', function(active_osm){
					var active_osm_found = _.find(this.osms.toJSON(), function(osm){
						return osm.name === active_osm.name;
					});

					this.active_osm = active_osm_found || this.active_osm;

				}, this);
			},
			render: function(){
				// Resetting view
				this.closeSubViews();
				this.$el.empty();

				// Initializing subviews
				this.$el.append(this.template({}));
				this.addSubView(new OsmsView({'osms': this.osms, el: this.$el.find('#osms') ,'vent': this.vent}));
				this.addSubView(new SwitchAreaView({data: this.data, el: this.$el.find('#switch-area') ,'vent': this.vent}));
				this.addSubView(new OrderView({data: this.active_osm, el: this.$el.find('#active-osm') ,'vent': this.vent}));


				// Rendering subviews
				_.each(this.subViews, function(view){
					view.render().el;
				}, this);

				return this;
			}
		});

		return ComparatorView;
})
