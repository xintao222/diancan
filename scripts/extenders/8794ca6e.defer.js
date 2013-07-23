define([
    'knockout-origin'
  ], function(
    ko
  ) {
'use strict';
return function(target) {
  return ko.extenders.throttle(target, 1);
};
});