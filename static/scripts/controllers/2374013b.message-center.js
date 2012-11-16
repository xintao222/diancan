define([
    'underscore',
    'backbone'
  ], function(
    _,
    Backbone
  ) {

'use strict';
var MessageCenter = _.extend({}, Backbone.Events);

MessageCenter.subscribe = MessageCenter.on;
MessageCenter.unsubscribe = MessageCenter.off;
MessageCenter.publish = MessageCenter.trigger;

return MessageCenter;

});