define([
    'config',
    'backbone'
  ], function(
    config,
    Backbone
  ) {
'use strict';

return Backbone.Model.extend({
  defaults: {
    'email': '',
    'name': ''
  },
  idAttribute: 'email',
  url: config.uri.USER
});

});