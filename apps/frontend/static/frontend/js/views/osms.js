define([
	'underscore',
	'views/base',
	'collections/osms',
	'text!../../templates/osm.html'
	], function(_, BaseView, OsmsCollection, osmTemplate){

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
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				var that = this;
				this.osms.each(function(osm){
					var data = osm.toJSON();
					that.$el.append(that.template(data));
				})

				return this;
			}
		});

		return ComparatorView;
})