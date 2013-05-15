define([
	'models/base'
	], function(BaseModel){

		var UserModel = BaseModel.extend({
			defaults:{
				is_active: false,
				username: 'se connecter',
				mail: ''
			},
			url: function(){
				if (this.prospect) return '/prospects';
				return '/api/auth/login/';
			},
			initialize: function(){
				this.prospect = false;
				console.log(this.vent);
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
				this.save({username: name, password: pass});
			},
			save: function(attributes, options){
				attributes || (attributes = {});
				var username = attributes.username || '';
				var password = attributes.password || '';
				options || (options = {});
				var vent = this.vent;
				var that = this;

				if(this.prospect){
					options.emulateJSON = true;
					options.data = {'mail': this.get('mail')};
				}else{
					options.emulateJSON = true;
					options.data = {
						'username': username,
						'password': password
					};
					options.success = function(data, textStatus, jqXHR){
						vent.trigger('user:authenticate:success');
						console.log(data);
						console.log(textStatus);
						console.log(jqXHR);
						console.log(that.toJSON());
					}
					options.error = function(jqXHR, textStatus, errorThrown){
						vent.trigger('user:authenticate:failure');
						console.log(jqXHR);
						console.log(textStatus);
						console.log(errorThrown);
					}
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		})


		return UserModel;
})