define([
	'views/base',
	'modernizr',
	'foundation',
	], function(BaseView){

		var LoginView = BaseView.extend({
			el: '#loginModal',
			initialize: function(){
				this.vent.on('user:403', this.show, this);
				this.vent.on('user:prospect:approve', this.approveProspect, this);
				this.vent.on('user:prospect:error', this.show, this);
				this.vent.on('user:authenticate:success', this.successAuthentication, this);
				this.vent.on('user:authenticate:failure', this.failureAuthentication, this);
				this.shown = false;
			},
			events: {
				// Authenticate user
				'click #sign-in-button': 'authenticate',
				'keypress #sign-in input': 'authenticate',

				// Prospect registration
				'click #invitation-button': 'invitation',
				'keypress .mail.prospect': 'invitation',
			},
			show: function(){
				if (!this.shown) this.$el.foundation('reveal', 'open');
				this.shown = true;
			},

			// Authentication related methods
			authenticate: function(event){
				if(event.type === 'keypress'){
					var code = event.charCode;
					if (code === 13){
						event.preventDefault();
						this.$el.find('#sign-in-button').trigger('click');
					}
				}else{
					var options={};
					options.name = this.$el.find('.form-container input[type=email]').val();
					options.pass = this.$el.find('.form-container input[type=password]').val();
					this.vent.trigger('user:authenticate', options);
				}
			},
			successAuthentication: function(){
				// this.vent.trigger('route:go:start');
				window.location.reload();
			},

			// Invitation related methods
			invitation: function(event){
				if(event.type === 'keypress'){
					var code = event.charCode;
					if (code === 13){
						event.preventDefault();
						this.$el.find('#invitation-button').trigger('click');
					}
				}else{
					var mail = this.$el.find('.mail.prospect').val();
					var mail_validator = /\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/i;
					if (mail_validator.test(mail)) {
						this.vent.trigger('user:prospect', {'mail': mail});
					}else{
						this.mailNotOk();
					}
				}

			},
			approveProspect: function(){
				this.$el.find('#successmessage, .errormessage').hide();
				this.$el.find('#successmessage').fadeIn();
			},
			errorProscpect: function(){
				this.$el.find('#successmessage, .errormessage').hide();
				this.$el.find('.errormessage').fadeIn();
			},
			mailNotOk: function(){
				this.$el.find('#successmessage, .errormessage').hide();
				this.$el.find('.mailnotok').fadeIn();
			}
		})

		return LoginView;
})