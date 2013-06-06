define([
	'underscore',
	'views/base',
	'views/switch-osm',
	'text!../../templates/switch.html'
], function(_, BaseView, SwitchOSMView, switchTemplate){

	var SwitchView = BaseView.extend({
		el: '#switch',
		template: _.template(switchTemplate),
		initialize: function(options){
			this.osms = options.osms;

			var that = this;

			this.bindTo(this.osms, 'add change', this.render);

			this.bindTo(this.osms, 'request', function(model, resp, xhr){
				that.$el.find('a.cta').hide();
				that.$el.find('.loader').show();
			});

			this.bindTo(this.osms, 'sync', function(model, resp, xhr){
				that.$el.find('a.cta').show();
				that.$el.find('.loader').hide();
			});


			this.bindTo(this.osms, 'add change', this.render);

			// Global events
			this.vent.on('view:switch:show', this.show, this);
			this.vent.on('view:switch:hide', this.hide, this);
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			this.$el.append(this.template({}));

			this.osms.each(function(osm){

				var view;
				if (osm.get('active')){
					view = new SwitchOSMView({'osm': osm, 'el': this.$el.find('.osms-switch-active'), 'vent': this.vent});
					view.render();

				}else{
					view = new SwitchOSMView({'osm': osm, 'vent': this.vent});
					this.$el.find('.inactive-area').append(view.render().el);
				}

			}, this);

			return this;
		},
		show: function(){
			this.$el.show();
		},
		hide: function(){
			this.$el.hide();
		},
		events: {
			'click .osms-switch-close': 'hide',
			'click .osms-switch-bg': 'hide',
		}
	});


	return SwitchView;
})