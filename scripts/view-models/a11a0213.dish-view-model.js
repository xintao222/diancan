define([
    'knockout'
  ], function(
    Knockout
  ) {
'use strict';
var DishViewModel = function(name, rest, amount, price) {
  var self = this;
  self.name = Knockout.observable(name || '');
  self.rest = Knockout.observable(rest || '');
  self.amount = Knockout.observable(amount || 1);
  self.price = Knockout.observable(price || 0);

  self.add = function(amount) {
    amount = amount || 1;
    self.amount(self.amount() + amount);
    return self;
  };

  self.minus = function() {
    self.amount(self.amount() - 1);
    return self;
  };

  self.equals = function(dish) {
    if (!(dish instanceof DishViewModel)) {
      return false;
    }
    if (self.name() === dish.name() &&
        self.rest() === dish.rest() &&
        self.price() === dish.price()) {
      return true;
    }
    else {
      return false;
    }
  };

  self.toJSON = function() {
    return {
      'name': self.name(),
      'from': self.rest(),
      'number': self.amount(),
      'price': self.price()
    };
  };
};

DishViewModel.filter = function(name, rest, dish) {
  return dish.name() === name && dish.rest() === rest;
};

return DishViewModel;

});