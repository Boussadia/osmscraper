define([
	'views/base',
	'views/subMenuItem',
	'collections/subMenu'
	], function(BaseView, SubMenuItemView, SubMenuCollection){

		var SubMenuView = BaseView.extend({
			tagName: 'ul',
			className: 'dropdown',
			initialize: function(options){
				options || (options = {});
				this.models = options.models || {};
				this.subMenuCollection = new SubMenuCollection(this.models, {'vent': this.vent});
				this.bindTo(this.subMenuCollection, 'reset', function(a, b){
					this.render();
				}, this);

				// Global Events binding
				this.vent.on('category:next:sub', this.next_sub_category, this);
				this.vent.on('route:category', this.activateSubMenuItem, this);
			},
			render: function(){
				this.closeSubViews();
				this.$el.empty();
				this.subMenuCollection.each(function(menuitem){
					this.addOne(menuitem);
				}, this)
				return this;
			},
			addOne: function(menuItem){
				var view = new SubMenuItemView({'model':menuItem, 'vent': this.vent});
				this.addSubView(view);
				this.$el.append(view.render().el);
			},
			activateSubMenuItem: function(options){
				options || (options = {});
				subMenuItem_id = options.id || null;

				if (subMenuItem_id !== null){
					
					_.any(this.subViews, function(view, index){
						var model = view.model;
						if(model.get('id') === subMenuItem_id){
							view.activate();
						}else{
							view.unactivate();
						}
					})
				}
			},
			get_category_id: function(categoryName){
				var result = this.subMenuCollection.findWhere({'url': categoryName}) || null;
				return result;
			},
			next_sub_category: function(obj){
				obj || (obj = {});
				var category_id = obj.id || null;
				var index_lookup = null;

				if (category_id){
					// Looking for sub category with id = category_id
					var that = this;
					this.subMenuCollection.each(function(model, i){
						if (model.id == category_id ) index_lookup = i;
					})
				}

				if(index_lookup != null){
					var next_index = index_lookup + 1;
					var count = this.subMenuCollection.length;
					if (next_index < count){
						this.subViews[next_index].click();
					}
				}else{

				}
			}
		});

		return SubMenuView;
})