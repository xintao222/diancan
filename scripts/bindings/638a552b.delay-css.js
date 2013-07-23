define([
    'knockout-origin',
    'underscore'
  ], function(
    ko,
    _
  ) {
'use strict';
return {
  update: function() {
    _.defer(function(args, context) {
      ko.bindingHandlers.css.update.apply(context, args);
    }, arguments, this);
  }
};

});