define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'views/categoryCollectionView'
], function($, _ , Backbone, Router, CategoryCollectionView){

	function App(){
		// Mustache style templatating
		_.templateSettings = {
			interpolate : /\{\{(.+?)\}\}/g
		};

		// Event dispatcher
		var vent = _.extend({}, Backbone.Events);
		this.vent = vent;

		// Events
		this.vent.on('route:index', this.index, this);
		this.vent.on('route:subcategory', this.subCategory, this);
		this.vent.on('render', this.render, this);

		this.init_data = parent_categories;
		this.viewsSubCategory = [];
	}

	App.prototype.subCategory = function(list_url){
		if(!this.parentCategoryView){
			this.parentCategoryView = new CategoryCollectionView({'init_data': this.init_data, 'vent': this.vent, 'level':-1, 'current_selected': list_url[0] });
		}else{
			this.parentCategoryView.set_current(list_url[0]);
		}

		// var start_index = 0;
		// for (var i=0; i<list_url;i++){
		// 	if(i<this.viewsSubCategory.length){

		// 	}
		// }

		// this.closeAfter(start_index);

		this.closeViews();

		// Creating new CategoryCollectionViews
		var i = 0;
		_.each(list_url, function(url){
			var current_selected = list_url[i+1];
			var view = new CategoryCollectionView({'url': url, 'vent': this.vent, 'level':i, 'parent_url': url, 'current_selected': current_selected});
			this.viewsSubCategory.push(view);
			view.fetch();
			i = i+1;
		}, this);
	}

	App.prototype.closeViewAt = function(index){
		if(this.viewsSubCategory[index]){
			this.viewsSubCategory[index].close();
			this.viewsSubCategory.pop(index);
		}
	}

	App.prototype.closeAfter = function(index_start){
		for (var i = index_start; i<this.viewsSubCategory.length; i++){
			this.closeViewAt(i);
		}
	}

	App.prototype.closeViews = function(){
		_.each(this.viewsSubCategory, function(view){
			view.close();
		}, this);
		this.viewsSubCategory = [];
	}

	App.prototype.index = function(option){
		this.render();

	}

	App.prototype.render = function(){
		if(!this.parentCategoryView){
			this.parentCategoryView = new CategoryCollectionView({'init_data': this.init_data, 'vent': this.vent, 'level':-1, 'current_selected': '' });
		}

		var rendered = this.parentCategoryView.render().el;
		var wraper = $('<div>');
		wraper.html(rendered);
		$('#content').html(wraper);

		$('.content').remove();

		var wraper = $('<div>').addClass('content');

		for (var i = 0; i < this.viewsSubCategory.length; i++) {
			var view = this.viewsSubCategory[i];
			if(view.fetched){
				wraper.append(view.render().el);
			}
		};

		$('#content').append(wraper);
		this.hijax();

	}

	App.prototype.initialize = function(){
		// Pass in our Router module and call it's initialize function
		this.router = new Router({'vent': this.vent});
		Backbone.history.start({
			root: '/backend'
		});
		this.hijax();

	};

	App.prototype.hijax = function(){
		var router = this.router;
		// Use absolute URLs  to navigate to anything not in your Router.
		// Only need this for pushState enabled browsers
		if (Backbone.history && Backbone.history._hasPushState) {

			// Use delegation to avoid initial DOM selection and allow all matching elements to bubble
			$(document).delegate("a:not(.no-hijax)", "click", function(evt) {
				// Get the anchor href and protcol
				var href = $(this).attr("href");
				var protocol = this.protocol + "//";
				// Ensure the protocol is not part of URL, meaning its relative.
				// Stop the event bubbling to ensure the link will not cause a page refresh.
				if (href.slice(protocol.length) !== protocol) {
					evt.preventDefault();

					// Note by using Backbone.history.navigate, router events will not be
					// triggered.  If this is a problem, change this to navigate on your
					// router.
					router.navigate(href, true);
				}
			});
		}

	}

	App.prototype.navigate = function(href){
		this.router.navigate(href, true);
	}

	App.prototype.getPreviousRoot = function(){
		if (this.router.history.length>1) {
			return this.router.history[this.router.history.length-2];
		};
	}

	return App;
});