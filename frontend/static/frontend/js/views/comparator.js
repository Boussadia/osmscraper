define([
	'underscore',
	'views/base',
	'views/osms',
	'views/switch-area',
	'collections/osms',
	'text!../../templates/comparator.html'
	], function(_, BaseView, OsmsView, SwitchAreaView, OsmsCollection, comparatorTemplate){

		var ComparatorView = BaseView.extend({
			el: '#comparator',
			template: _.template(comparatorTemplate),
			TRIGGER: 138,
			initialize: function(options){
				this.osms = options.osms || new OsmsCollection([], {'vent': this.vent});
				this.render();

				this.vent.on('carts', function(carts){

					// Getting active osm
					var active_osm = _.find(carts, function(cart){
						return cart.active;
					});
					
					// Getting cart with minimum cart price
					var min = _.min(carts, function(cart){
						return cart.price
					});

					// Setting price to save
					try{
						this.data = {
							price_to_save: - (active_osm.price-min.price),
						}
					}catch(e){
						console.log(e);
					}

					this.render();
				},this);
			},
			render: function(){
				// Resetting view
				this.closeSubViews();
				this.$el.empty();

				// Initializing subviews
				this.$el.append(this.template({}));
				this.addSubView(new OsmsView({'osms': this.osms, el: this.$el.find('#osms') ,'vent': this.vent}));
				this.addSubView(new SwitchAreaView({data: this.data, el: this.$el.find('#switch-area') ,'vent': this.vent}));


				// Rendering subviews
				_.each(this.subViews, function(view){
					view.render().el;
				}, this);

				return this;
			}
		});

		return ComparatorView;
})
