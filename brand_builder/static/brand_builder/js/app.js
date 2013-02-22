define([
	'jquery',
	'underscore',
	'backbone',
	'router',
	'views/brandCollectionView'
], function($, _ , Backbone, Router, BrandCollectionView){

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
		this.vent.on('route:subBrand', this.subBrand, this);
		this.vent.on('render', this.render, this);

		this.init_data = parent_brands;
		this.viewsSubBrand = [];
	}

	App.prototype.subBrand = function(list_url){
		if(!this.parentBrandView){
			this.parentBrandView = new BrandCollectionView({'init_data': this.init_data, 'vent': this.vent, 'level':-1, 'current_selected': list_url[0] });
		}else{
			this.parentBrandView.set_current(list_url[0]);
			// this.parentBrandView.fetch();
		}

		this.closeViews();

		// Creating new BrandCollectionViews
		var i = 0;
		_.each(list_url, function(url){
			var current_selected = list_url[i+1];
			var view = new BrandCollectionView({'url': url, 'vent': this.vent, 'level':i, 'parent_url': url, 'current_selected': current_selected});
			this.viewsSubBrand.push(view);
			view.fetch();
			i = i+1;
		}, this);
	}

	App.prototype.closeViewAt = function(index){
		if(this.viewsSubBrand[index]){
			this.viewsSubBrand[index].close();
			this.viewsSubBrand.pop(index);
		}
	}

	App.prototype.closeAfter = function(index_start){
		for (var i = index_start; i<this.viewsSubBrand.length; i++){
			this.closeViewAt(i);
		}
	}

	App.prototype.closeViews = function(){
		_.each(this.viewsSubBrand, function(view){
			view.close();
		}, this);
		this.viewsSubBrand = [];
	}

	App.prototype.index = function(option){
		this.render();

	}

	App.prototype.render = function(){
		if(!this.parentBrandView){
			this.parentBrandView = new BrandCollectionView({'init_data': this.init_data, 'vent': this.vent, 'level':-1, 'current_selected': '' });
		}

		var rendered = this.parentBrandView.render().el;
		var wraper = $('<div>');
		wraper.html(rendered);
		$('#content').html(wraper);

		$('.content').remove();

		var wraper = $('<div>').addClass('content');

		for (var i = 0; i < this.viewsSubBrand.length; i++) {
			var view = this.viewsSubBrand[i];
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
			root: '/backend/brand'
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