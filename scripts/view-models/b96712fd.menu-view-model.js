define([
    'knockout',
    'jquery',
    'config',
    'backbone',
    'underscore'
  ], function(
    Knockout,
    jQuery,
    config,
    Backbone,
    _
  ) {
'use strict';

var MenuViewModel = function() {
  var self = this;
  _.extend(self, Backbone.Events);
  self.menu = Knockout.observableArray();
  self.categories = Knockout.computed(function() {
    return self.menu().map(function(group) {
      return group.category;
    });
  });
  self.dishes = Knockout.computed(function() {
    var dishes = [];
    self.menu().forEach(function(group) {
      group.dishes.forEach(function(dish) {
        dishes.push(dish.name);  
      });
    });
    // return JSON.stringify(dishes);
    return dishes;
  });
  self.selectedCategory = Knockout.observable({
    dishes: []
  });

  self.fetch = function(url) {
    return jQuery.get(config.buildMenuURI(url)).pipe(function(data) {
      return self.menu(data).selectedCategory(data[0]);
    });
  };

  self.order = function(data) {
    self.trigger('order', data.name, data.price);
  };
};

return MenuViewModel;
});