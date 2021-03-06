define([
	'underscore',
	'jquery',
	'backbone',
	'bootstrap',
	'views/categoryView',
	'views/baseView',
	'collections/categoryCollection'
	], function(_, $, Backbone, Bootstrap, CategoryView, BaseView, CategoryCollection){
		var CategoryCollectionView = BaseView.extend({
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
			template: $('#template_category_list').text(),
			render: function(){
				var content = '';
				var $tbody = $('<tbody>');
				_.each(this.categoryCollection.models, function(model){
					var model_json = model.toJSON()
					var url_identifier = model_json['url'].split(model_json['parent_url']+'/').pop();
					var view = new CategoryView({'model': model, 'is_current': (this.current_selected == url_identifier)});
					this.addSubView(view);

					$tbody.append(view.render().el);

				}, this);


				this.$el.append($tbody);

				var that = this;
				this.$el.find('button.remove').click(function(e){
					e.preventDefault();
					that.removeCategory(e);
				});
				if(this.level>-1){
					var button = $("#add_category").text();
					this.$el.append(button);
					this.$el.find('button.add').click(function(e){
						e.preventDefault();
						that.modal();
					});
				}else{
					// this.$el.find('.remove').remove();
				}
				return this;

			},
			initialize: function(option){
				this.vent = option.vent || null;
				this.init_data = option.init_data || null;
				this.level = option.level;
				this.url = option.url || null;
				this.parent_url = option.parent_url;
				this.current_selected = option.current_selected;
				this.categoryCollection = new CategoryCollection(this.init_data);
				this.categoryCollection.set_url(this.url);
				this.categoryCollection.set_parent_url(this.parent_url);
				this.bindTo(this.categoryCollection, 'reset', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
				this.bindTo(this.categoryCollection, 'add', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
				this.bindTo(this.categoryCollection, 'remove', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
			},
			fetch : function(){
				this.fetched = false;
				this.categoryCollection.fetch();
			},
			events: {
				// 'click button.add': 'modal',
				// 'click button.btn-close': 'closeModal',
				// 'click button.save': 'saveCategory',
				// 'click button.remove': 'removeCategory',
			},
			removeCategory: function(e){
				if(confirm('Si vous supprimer cette categorie, toutes les categories filles vont être suprimée, voulez vous proceder?')){
					var id = $(e.target).attr('data-id');
					if(!id){
						var id = $(e.target).parent().attr('data-id');

					}
					this.categoryCollection.removeFromServer(id);
				}
			},
			modal: function(){
				var modal_html = $('#modal').text();
				var modal_template = _.template(modal_html);
				var modal_rendered = modal_template({'level': this.level, 'parent_url': this.parent_url});
				this.$el.append(modal_rendered);
				var that = this;
				this.$el.keypress(function(e){
					if(e.keyCode == 13){
						that.saveCategory(e);
					};
					if(e.keyCode == 27){
						that.closeModal(e);
					};
				})
				this.$el.find("button.btn-close").click(function(e){
						e.preventDefault();
						that.closeModal(e);
					});
				this.$el.find("button.save").click(function(e){
						e.preventDefault();
						that.saveCategory(e);
					});
			},
			closeModal: function(e){
				e.preventDefault();
				this.$el.find("#form_"+this.level).remove();
				this.$el.find('.modal-backdrop').remove();
			},
			saveCategory: function(e){
				e.preventDefault();
				var name = this.$el.find('#name_category').val();
				var url = this.$el.find('#url_category').val();
				this.categoryCollection.addNewCategory({'name': name, 'url': url});
			},
			set_current: function(url_current){
				this.current_selected = url_current;
			}
		});
		return CategoryCollectionView;

})