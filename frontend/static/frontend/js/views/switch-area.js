define([
	'views/base',
	'text!../../templates/switch-area.html'
],function(BaseView, switchAreaTemplate){

	var SwitchArea = BaseView.extend({
		el: '#switch-area',
		template:  _.template(switchAreaTemplate),
		initialize: function(options){
			this.data = {
				price_to_save: 0,
			}
			this.data = options.data || this.data;
		},
		render: function(){
			this.$el.empty();
			this.$el.append(this.template(this.data));
			return this;
		}
	})

	// var SaveAndOrderView = MenuItemView.extend({
	// 	mainTemplate: _.template(saveAndOrderTemplate),
	// 	initialize: function(options){
	// 		this.data = {
	// 			price_to_save: 0,
	// 			price_cart: 0
	// 		}
	// 		// ORDER BUTTON
	// 		var data = {
	// 			'url': 'monoprix',
	// 			'name': 'monoprix'
	// 		}
	// 		this.orderView = new OrderView({'model': data,  'vent': this.vent});

	// 		this.vent.on('carts', function(carts){
	// 			var current = this.orderView.model['name'];
	// 			var price = carts[current].price;

	// 			var min = price;

	// 			for (var i in carts){
	// 				if (carts[i].price<min) min = carts[i].price;
	// 			}

	// 			this.data = {
	// 				price_to_save: min - price,
	// 				price_cart: price
	// 			}
	// 			this.render();
	// 		},this);

	// 		this.vent.on('osm', function(osm){
	// 			this.orderView.model = {
	// 				'url': osm['name'],
	// 				'name': osm['name']
	// 			}
	// 			this.orderView.render();
	// 		}, this);

	// 	},
	// 	render: function(){
	// 		this.$el.empty();
	// 		this.$el.append(this.mainTemplate(this.data));
	// 		this.$el.hide();
	// 		return this;
	// 	},
	// 	showSubMenu: function(e){
	// 		// TODO OVERWRITE DEFAULT BEHAVIOR
	// 	}
	// })

	// return SaveAndOrderView;


	return SwitchArea;

})