require.config({
  shim: {
    backbone: {
      deps: ['underscore'],
      exports: 'Backbone'
    },
    underscore: {
      exports: '_'
    }
  },

  paths: {
    jquery: 'vendor/jquery.fake',
    backbone: 'vendor/backbone',
    underscore: 'vendor/underscore',
    // knockout: 'vendor/knockout'
    knockout: 'vendor/knockout-latest.debug',
    knockback: 'vendor/knockback'
  }
});

require(['app'], function(app) {
  'use strict';
  // use app here
});