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
				var content = ''
				_.each(this.categoryCollection.models, function(model){
					var view = new CategoryView({'model': model});
					this.addSubView(view);
					content = content +' '+view.render().el;
				}, this);
				var template = _.template(this.template);
				content = template({'content': content});
				this.$el.html(content);
				if(this.level>-1){
					var button = $("#add_category").text();
					this.$el.append(button);
				}
				return this;

			},
			initialize: function(option){
				this.vent = option.vent || null;
				this.init_data = option.init_data || null;
				this.level = option.level;
				this.url = option.url || null;
				this.parent_url = option.parent_url;
				this.categoryCollection = new CategoryCollection(this.init_data);
				this.categoryCollection.set_url(this.url);
				this.bindTo(this.categoryCollection, 'reset', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
				this.bindTo(this.categoryCollection, 'add', function(){
					this.fetched = true;
					this.vent.trigger('render');
				});
			},
			fetch : function(){
				this.fetched = false;
				this.categoryCollection.fetch();
			},
			events: {
				'click button.add': 'modal',
				'click button.btn-close': 'closeModal',
				'click button.save': 'saveCategory'
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
			saveCategory: function(e){
				e.preventDefault();
				var name = this.$el.find('#name_category').val();
				var url = this.$el.find('#url_category').val();
				this.categoryCollection.addNewCategory({'name': name, 'url': url});
			}
		});
		return CategoryCollectionView;

})