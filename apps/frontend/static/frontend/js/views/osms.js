define([
	'underscore',
	'views/base',
	'views/order',
	'collections/osms',
	'text!../../templates/osm.html'
	], function(_, BaseView, OrderView, OsmsCollection, osmTemplate){

		var ComparatorView = BaseView.extend({
			el: 'div#osms',
			template: _.template(osmTemplate),
			TRIGGER: 138,
			initialize: function(options){
				this.osms = options.osms || new OsmsCollection([], {'vent': this.vent});
				var that = this;
				this.bindTo(this.osms, 'request', function(){
					that.$el.find('.loader').show();
					that.$el.find('.loader+p').hide();
				});

				this.bindTo(this.osms, 'sync', function(){
					that.$el.find('.loader').hide();
					that.$el.find('.loader+p').show();
				});

				this.bindTo(this.osms, 'change', this.render);
			},
			events: {
				'click .osm': 'showModal',
			},
			render: function(){
				this.closeSubViews();
				var that = this;
				var order_view = new OrderView({'osms': this.osms, el: this.$el.find('#active-osm') ,'vent': this.vent});
				order_view.render();
				this.addSubView(order_view);
				this.osms.each(function(osm){
					var data = osm.toJSON();
					that.$el.find('div#non-active-osm').append(that.template(data));
				})

				return this;
			},
			showModal: function(e){
				this.vent.trigger('view:switch:show');
			}
		});

		return ComparatorView;
})