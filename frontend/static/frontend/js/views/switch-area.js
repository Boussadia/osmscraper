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
	});
	
	return SwitchArea;

})