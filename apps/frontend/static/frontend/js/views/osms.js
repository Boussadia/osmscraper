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
					that.showLoader();
				});

				this.bindTo(this.osms, 'sync', function(){
					that.hideLoader();
				});

				this.vent.on('product:request', this.showLoader, this);

				this.bindTo(this.osms, 'change', this.render);
			},
			events: {
				'click .osm': 'showModal',
			},
			render: function(){
				this.closeSubViews();
				this.$el.find('div#non-active-osm').empty();
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
			},
			showLoader: function(){
				this.$el.find('.loader').show();
				this.$el.find('.loader+p').hide();
			},
			hideLoader: function(){
				this.$el.find('.loader').hide();
				this.$el.find('.loader+p').show();
				
			}
		});

		return ComparatorView;
})