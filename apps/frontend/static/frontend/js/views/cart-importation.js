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
			this.osms = options.osms;
			this.selected_osm = this.osms.get_active_osm().get('name');
			var that = this;
			this.bindTo(this.importModel, 'request', function(){
				that.fetching = true;
				that.$el.find('.import-loader-bg').show();
				that.$el.find('#import-loader').show();
			})
			this.bindTo(this.importModel, 'sync', function(){
				that.fetching = false;
				that.hide();
				that.vent.trigger('cart:newproduct');
				that.$el.find('.import-loader-bg').hide();
				that.$el.find('#import-loader').hide();
			})
			this.vent.on('modal:show:import', this.show, this);
		},
		events: {
			'click a.close-reveal-modal': 'hide',
			'click .reveal-modal-bg': 'hide',
			'click #sign-in-button': 'import',
			'keypress input': 'enterListener',
			'click #osms td': 'set_osm'
		},
		render: function(){
			this.closeSubViews();
			this.$el.empty();
			var data = [];
			data['osms'] = this.osms.toJSON();
			var rendered = this.template(data);
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
			this.importModel.set('osm', this.selected_osm);
			this.importModel.save();
		},
		enterListener: function(event){
			if(event.type === 'keypress'){
				var code = event.charCode;
				if (code === 13){
					event.preventDefault();
					this.$el.find('#sign-in-button').trigger('click');
				}
			}
		},
		set_osm: function(e){
			var $element = $(e.target).parent();
			this.$el.find('.active').removeClass('active');
			this.selected_osm = $element.attr('class').replace(/\s+/g, '');;
			$element.addClass('active');
		}
	});


	return CartImportationView;

});