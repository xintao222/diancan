define([
    'models/user'
  ], function(
    User
  ) {
'use strict';
// Initializing global models
var data = {
  user: new User()
};
return {
  get: function(name) {
    if (name in data) {
      return data[name];
    }
    else {
      throw new Error('Unregistered data name: ' + name + '!');
    }
  }
};

});