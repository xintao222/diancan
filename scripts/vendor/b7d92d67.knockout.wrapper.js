define([
    'knockout-origin',
    'bindings/delay-css',
    'extenders/defer'
  ], function(
    ko,
    DelayCssBinding,
    DeferExtenders
  ) {
'use strict';
ko.bindingHandlers.delayCss = DelayCssBinding;
ko.extenders.defer = DeferExtenders;

return ko;
});