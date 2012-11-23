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
  var rests = ko.observableArray();
  rests.fetch = function() {
    return $.get(config.uri.RESTAURANTS).pipe(function(data) {
      rests(data);
      return rests;
    });
  };
  return rests;
};

});