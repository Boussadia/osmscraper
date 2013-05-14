define([
	'models/base'
	], function(BaseModel){

		var UserModel = BaseModel.extend({
			defaults:{
				authenticated: false,
				name: 'se connecter',
				mail: ''
			},
			url: function(){
				if (this.prospect) return '/prospects';
				return '/api/auth/login/';
			},
			initialize: function(){
				this.prospect = false;
				this.vent.on('user:prospect', this.registerProspect, this);
				this.vent.on('user:authenticate', this.authenticate, this);
			},
			registerProspect: function(options){
				var mail = options.mail;
				this.prospect = true;
				this.set('mail', mail);
				var that = this;
				this.save({}, {
					success: function(){
						that.vent.trigger('user:prospect:approve');
						that.prospect = false;
					},
					error: function(){
						that.vent.trigger('user:prospect:error');
					}
				});
			},
			authenticate: function(options){
				var name = options.name;
				var pass = options.pass;
				this.set('name', name);
				this.set('pass', pass);
				this.save();
			},
			save: function(attributes, options){
				options || (options = {});
				var vent = this.vent;

				if(this.prospect){
					options.emulateJSON = true;
					options.data = {'mail': this.get('mail')};
				}else{
					options.emulateJSON = true;
					options.data = {
						'username': 'ahmed',
						'password': '2asefthukom,3'
					};
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		})


		return UserModel;
})