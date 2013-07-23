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
    'knockout-origin': 'vendor/knockout-latest.debug',
    knockout: 'vendor/knockout.wrapper',
    knockback: 'vendor/knockback'
  }
});

require(['app'], function() {
  'use strict';
  // use app here
});
