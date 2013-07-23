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
      'ORDER': host + '/api/order',
      'DEFAULT': host + '/api/default',
      'DESTORY': host + '/api/delorder'
    },

    buildMenuURI: function(url) {
      return this.HOST + '/api/' + url;
    }
  };

});
