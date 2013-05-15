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

				this.bindTo(this.osms, 'change', this.render);
				// this.vent.on('window:scroll', this.set_fixed_position, this);
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
			},
			set_fixed_position: function(){
				var scrollTop = $(window).scrollTop();
				var parent = this.$el.parent();
				if(scrollTop>this.TRIGGER){
					parent.addClass('top');
					// parent.css('top',(scrollTop-7)+'px');
				}else if(scrollTop<=this.TRIGGER){
					parent.removeClass('top');
					// parent.css('top', '0px');
				}
			}
		});

		return ComparatorView;
})