define([
	'underscore',
	'backbone'
	], function(_, Backbone){

		var BaseView = function (options) {
			this.bindings = [];
			this.subViews = [];
			options || (options = {});
			this.vent = options.vent || {};
			
			Backbone.View.apply(this, [options]);
		};

		_.extend(BaseView.prototype, Backbone.View.prototype, {
			bindTo: function (model, ev, callback) {
				model.bind(ev, callback, this);
				this.bindings.push({ model: model, ev: ev, callback: callback });
			},
			addSubView: function(subView, position){
				position || (position = this.subViews.length);
				this.subViews.splice(position, 0, subView);
			},
			unbindFromAll: function () {
				_.each(this.bindings, function (binding) {
					binding.model.unbind(binding.ev, binding.callback);
				});
				this.bindings = [];
			},
			close: function () {
				if(this.beforeClose){
					// If an action needs to be executed before closing the view
					this.beforeClose();
				}
				this.closeSubViews();
				this.unbindFromAll();	// Will unbind all events this view has bound to
				this.unbind();			// This will unbind all listeners to events from 
										// this view. This is probably not necessary 
										// because this view will be garbage collected.
				this.remove();			// Uses the default Backbone.View.remove() method which
										// removes this.el from the DOM and removes DOM events.
			},
			closeSubViews: function(){
				_.each(this.subViews, function(subView){
					subView.close();
				});
				this.subViews = [];
			}
		});

		BaseView.extend = Backbone.View.extend;

		return BaseView;

})