define([
	'views/base',
	'text!../../templates/switch-area.html'
],function(BaseView, switchAreaTemplate){

	var SwitchArea = BaseView.extend({
		el: '#switch-area',
		template:  _.template(switchAreaTemplate),
		initialize: function(options){
			this.osms = options.osms;
			this.bindTo(this.osms, 'change', this.render);
		},
		render: function(){
			this.$el.empty();
			var data = {
				price_to_save: this.osms.get_price_to_save()
			}
			this.$el.append(this.template(data));

			return this;
		},
		events: {
			'click .cta.comparer': 'showSwitcher'
		},
		showSwitcher: function(event){
			this.vent.trigger('view:switch:show');
		}
	});
	
	return SwitchArea;

})