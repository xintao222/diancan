define([
    'knockout',
    'underscore'
  ], function(
    ko,
    _
  ) {
'use strict';
return (function() {
  var timer;
  var self = _.extend(function(message) {
    self.message(message);
  }, {
    message: ko.observable(''),
    clear: function() {
      self.message('');
    }
  });
  self.message.subscribe(function(value) {
    if (!value) {
      return;
    }
    clearTimeout(timer);
    timer = _.delay(function() {
      self.clear(timer);
    }, 5000);
  });
  return self;
})();

});