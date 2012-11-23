define([
    'knockout',
    'underscore'
  ], function(
    ko,
    _
  ) {
'use strict';
ko.bindingHandlers.delayCss = {
    update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
      _.defer(function(args, context) {
        ko.bindingHandlers.css.update.apply(context, args);
      }, arguments, this);
    }
};

}); 