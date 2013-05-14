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
				return '/prospects';
			},
			initialize: function(){
				this.prospect = false;
				this.vent.on('user:prospect', this.registerProspect, this);
			},
			registerProspect: function(options){
				var mail = options.mail;
				this.prospect = true;
				this.set('mail', mail);
				var that = this;
				this.save({}, {
					success: function(){
						that.vent.trigger('user:prospect:approve');
					},
					error: function(){
						that.vent.trigger('user:prospect:error');
					}
				});
			},
			save: function(attributes, options){
				options || (options = {});
				var vent = this.vent;

				if(this.prospect){
					options.emulateJSON = true;
					// options.emulateHTTP = true;
					options.data = {'mail': this.get('mail')};
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		})


		return UserModel;
})