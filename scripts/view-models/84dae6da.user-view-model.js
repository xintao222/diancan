define([
    'knockout',
    'jquery',
    'config'
  ], function(
    Knockout,
    jQuery,
    config
  ) {
'use strict';
var UserViewModel = function() {
  var self = this;
  self.id = Knockout.observable();
  self.name = Knockout.observable();
  self.name.subscribe(function(value) {
    localStorage.setItem('user-display-name', value);
  });
  self.online = Knockout.computed(function() {
    return !!self.id();
  });
  self.nameAbsent = Knockout.computed(function() {
    return self.online() && !self.name();
  });
  self.ready = Knockout.computed(function() {
    return !!(self.id() && self.name());
  });

  self.fetch = function() {
    return jQuery.get(config.uri.USER, function(data) {
      self.name(data.name).id(data.email);
    }).pipe(function() {
      return self;
    });
  };

  self.save = function(name) {
    return jQuery.post(config.uri.USER, {
      id: self.id(),
      name: name || self.name()
    }).pipe(function(data) {
      return self.id(data.email).name(data.name);
    });
  };
};

return new UserViewModel();

});