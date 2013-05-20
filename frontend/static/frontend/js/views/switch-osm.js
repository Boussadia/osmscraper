define([
	'underscore',
	'views/base',
	'text!../../templates/switch-osm.html'
], function(_, BaseView, switchOSMTemplate){

	var SwitchOSMView = BaseView.extend({
		className: 'osms-switch-inactive',
		template: _.template(switchOSMTemplate),
		initialize: function(options){
			this.osm = options.osm;
		},
		render: function(){
			this.$el.empty();
			var data = this.osm.toJSON();
			var template = this.template(data);
			this.$el.append(template);
			return this;
		},
		events:{
			'click .cta.comparer': 'switchToThisOSM'
		},
		switchToThisOSM: function(){
			this.osm.set('active', true);
			this.osm.save();
			this.vent.trigger('osm', this.osm.toJSON());
			this.vent.trigger('view:switch:hide');
		}
	});

	return SwitchOSMView;
})