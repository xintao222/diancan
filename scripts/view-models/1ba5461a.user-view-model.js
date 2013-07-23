define([
    'knockout',
    'jquery',
    'config',
    'knockback'
  ], function(
    ko,
    jQuery,
    config,
    kb
  ) {
'use strict';

return kb.ViewModel.extend({
  constructor: function() {
    var self = this;
    kb.ViewModel.prototype.constructor.apply(self, arguments);
    self.online = ko.computed(function() {
      return !!self.email();
    });
    self.nameAbsent = ko.computed(function() {
      return self.online() && !self.name();
    }).extend({ defer: true });
    self.ready = ko.computed(function() {
      return !!(self.email() && self.name());
    }).extend({ defer: true });
  },
  save: function(name) {
    return jQuery.post(config.uri.USER, {
      id: this.id(),
      name: name || this.name()
    }).pipe(function(data) {
      return this.id(data.email).name(data.name);
    }.bind(this));
  }
});

});