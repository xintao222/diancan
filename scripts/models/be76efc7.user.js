define([
    'knockout',
    'jquery',
    'config'
  ], function(
    ko,
    $,
    config
  ) {
'use strict';
return function() {
  var user = {
    id: ko.observable(),
    name: ko.observable() 
  };
  ko.subscribable.call(user);
  user.online = ko.computed(function() {
    return !!user.id();
  });
  user.infoAbsent = ko.computed(function() {
    return user.online() && !user.name();
  });
  user.ready = ko.computed(function() {
    return user.online() && !user.infoAbsent();
  });

  user.fetch = function() {
    return $.get(config.uri.USER).pipe(function(data) {
      user.id(data.email).name(data.name);
      return user;
    });
  };

  user.save = function() {
    return $.post(config.uri.USER, { name: user.name() }).pipe(function(data) {
      user.id(data.email).name(data.name);
      return user;
    });
  };
  return user;
};

});