define([
	'underscore',
	'jquery',
	'backbone',
	'bootstrap',
	'views/brandView',
	'views/baseView',
	'collections/brandCollection'
	], function(_, $, Backbone, Bootstrap, BrandView, BaseView, BrandCollection){
		var BrandCollectionView = BaseView.extend({
			tagName: 'table',
			attributes: function(){
				var level = this.level;
				return {
					'class': 'table table-hover',
					'data-level': level
				}
			},
			fetched: true,
			level: -1,
			template: $('#template_brand_list').text(),
			render: function(){
				var content = ''
				_.each(this.brandCollection.models, function(model){
					var model_json = model.toJSON();
					var url_identifier = model_json['url'].split(model_json['parent_url']+'/').pop();
					var view = new BrandView({'model': model, 'is_current': (this.current_selected == url_identifier)});
					this.addSubView(view);
					content = content +' '+view.render().el;
				}, this);
				var template = _.template(this.template);
				content = template({'content': content});
				this.$el.html(content);
				var button = $("#add_brand").text();
				this.$el.append(button);
				return this;

			},
			initialize: function(option){
				this.url = option.url || null;
				this.vent = option.vent || null;
				this.init_data = option.init_data || null;
				this.level = option.level;
				this.parent_url = option.parent_url;
				this.current_selected = option.current_selected;
				this.brandCollection = new BrandCollection(this.init_data);
				this.brandCollection.set_url(this.url);
				this.bindTo(this.brandCollection, 'reset', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
				this.bindTo(this.brandCollection, 'add', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
				this.bindTo(this.brandCollection, 'remove', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
			},
			fetch : function(){
				this.fetched = false;
				this.brandCollection.fetch();
			},
			events: {
				'click button.add': 'modal',
				'click button.btn-close': 'closeModal',
				'click button.save': 'saveBrand',
				'click button.remove': 'removeBrand',
			},
			removeBrand: function(e){
				if(confirm('Si vous supprimer cette marque, toutes les marques filles vont être suprimée, voulez vous proceder?')){
					var id = $(e.target).attr('data-id');
					if(!id){
						var id = $(e.target).parent().attr('data-id');

					}
					this.brandCollection.removeFromServer(id);
				}
			},
			modal: function(){
				var modal_html = $('#modal').text();
				var modal_template = _.template(modal_html);
				var modal_rendered = modal_template({'level': this.level, 'parent_url': this.parent_url});
				this.$el.append(modal_rendered);
			},
			closeModal: function(e){
				e.preventDefault();
				this.$el.find("#form_"+this.level).remove();
				this.$el.find('.modal-backdrop').remove();
			},
			saveBrand: function(e){
				e.preventDefault();
				var name = this.$el.find('#name_brand').val();
				var id = this.$el.find('#id_brand').val();
				if (!id) id = -1;
				console.log(id);
				this.brandCollection.addNewBrand({'name': name, 'id': id});
			},
			set_current: function(id_current){
				this.current_selected = id_current;
			}
		});
		return BrandCollectionView;

})