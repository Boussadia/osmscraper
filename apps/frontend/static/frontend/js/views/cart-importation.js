define([
	'underscore',
	'views/base',
	'models/cart-importation',
	'text!../../templates/import.html'
], function(_, BaseView, CartImportationModel, importTemplate){


	var CartImportationView = BaseView.extend({
		template: _.template(importTemplate),
		initialize: function(options){
			this.importModel = new CartImportationModel({}, {'vent': this.vent});
			this.fetching = false;
			var that = this;
			this.bindTo(this.importModel, 'request', function(){
				that.fetching = true;
			})
			this.bindTo(this.importModel, 'sync', function(){
				that.fetching = false;
				that.vent.trigger('cart:newproduct');
			})
			this.vent.on('modal:show:import', this.show, this);
		},
		events: {
			'click a.close-reveal-modal': 'hide',
			'click .reveal-modal-bg': 'hide',
			'click #sign-in-button': 'import',
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var rendered = this.template({});
			this.$el.append(rendered);
			return this;
		},
		show: function(options){
			this.$el.show();
		},
		hide: function(e){
			if (!this.fetching) this.$el.hide();
		},
		import: function(e){
			var mail = this.$el.find('input[type="email"]').val();
			var pass = this.$el.find('input[type="password"]').val();
			this.importModel.set('email', mail);
			this.importModel.set('password', pass);
			this.importModel.save();
		}
	});


	return CartImportationView;

});