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
					console.log(this.osms);
					var min = this.osms.models.min(function(osm){
						console.log(osm.price);
						return osm.price
					});
					console.log(min);

					// var min = price;

					// for (var i in carts){
					// 	if (carts[i].price<min) min = carts[i].price;
					// }

					// this.data = {
					// 	price_to_save: min - price,
					// }

					this.render();
				},this);

				// this.vent.on('osm', function(osm){
				// 	this.orderView.model = {
				// 		'url': osm['name'],
				// 		'name': osm['name']
				// 	}
				// 	this.orderView.render();
				// }, this);
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