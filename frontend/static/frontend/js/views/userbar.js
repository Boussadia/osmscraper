define([
	'views/base',
	'models/user',
	'text!../../templates/userbar.html',
	'dropit'
	], function(BaseView, UserModel, userBarTemplate){

		var UserBarView = BaseView.extend({
			el: '#profile-button',
			template: _.template(userBarTemplate),
			initialize: function(options){
				var user = options.user || new UserModel({}, {'vent': this.vent})
				this.user = user;
				this.bindTo(this.user, 'change', this.render);
			},
			render: function(){
				this.$el.empty();
				var data = this.user.toJSON();
				this.$el.append(this.template(data));

				this.$el.find('#top-icon-play').dropit({
					submenuEl: 'ul',
					triggerEl: 'img',
					triggerParentEl: 'div'
				})
				return this;
			},
			events: {
				// Dropdown
				'click #logout': 'logout',
			},
			logout: function(event){
				this.user.logout();
			}

		});

		return UserBarView;

})