define([
    'knockout',
    'config',
    'jquery',
    'underscore',
    'backbone'
  ], function(
    Knockout,
    config,
    jQuery,
    _,
    Backbone
  ) {
  'use strict';
  var RestaurantsViewModel = function() {
    var self = this;
    _.extend(self, Backbone.Events);
    // Raw data, from server.
    self.list = Knockout.observableArray();
    self.selectedRest = Knockout.observable();
    self.selectedRestName = Knockout.observable();
    self.selectedRestMenuURL = Knockout.observable();

    self.list.subscribe(function(newList) {
      self.select(newList[0]);
    });
    self.selectedRestMenuURL.subscribe(function(newURL) {
      self.trigger('change-menu', newURL);
    });

    self.select = function(rest) {
      self.selectedRest(rest);
      self.selectedRestName(rest.name);
      self.selectedRestMenuURL(rest.url);
      return self;
    };

    self.fetch = function() {
      return jQuery.get(config.uri.RESTAURANTS, self.list.bind(self)).pipe(function() {
        return self;
      });
    };
  };

  return RestaurantsViewModel;
});