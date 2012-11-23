define([

], function(

) {
  'use strict';

  var host = 'http://fan.wandoulabs.com';

  return {
    'HOST': host,
    uri: {
      'RESTAURANTS': host + '/api/all',
      'USER': host + '/api/user',
      'ORDER': host + '/order',
      'DEFAULT': host + '/api/default'
    },

    buildMenuURI: function(url) {
      return this.HOST + '/' + url;
    }
  };

});