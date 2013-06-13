define([
	'underscore',
	'views/base',
	'models/cart-export',
	'text!../../templates/export.html'
], function(_, BaseView, CartExportModel, exportTemplate){


	var CartExportView = BaseView.extend({
		template: _.template(exportTemplate),
		initialize: function(options){
			this.exportModel = new CartExportModel({}, {'vent': this.vent});
			this.fetching = false;
			var that = this;
			this.bindTo(this.exportModel, 'request', function(){
				that.fetching = true;
				that.$el.find('.import-loader-bg').show();
				that.$el.find('#import-loader').show();
			})
			this.bindTo(this.exportModel, 'sync', function(){
				that.fetching = false;
				that.hide();
				that.vent.trigger('cart:newproduct');
				that.$el.find('.import-loader-bg').hide();
				that.$el.find('#import-loader').hide();
			})
			this.vent.on('modal:show:export', this.show, this);
		},
		events: {
			'click a.close-reveal-modal': 'hide',
			'click .reveal-modal-bg': 'hide',
			'click #sign-in-button': 'export',
			'keypress input': 'enterListener',
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
		export: function(e){
			var mail = this.$el.find('input[type="email"]').val();
			var pass = this.$el.find('input[type="password"]').val();
			this.exportModel.set('email', mail);
			this.exportModel.set('password', pass);
			this.exportModel.save();
		},
		enterListener: function(event){
			if(event.type === 'keypress'){
				var code = event.charCode;
				if (code === 13){
					event.preventDefault();
					this.$el.find('#sign-in-button').trigger('click');
				}
			}
		}
	});


	return CartExportView;

});