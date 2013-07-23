define([
    'knockout',
    'view-models/dish-view-model',
    'underscore',
    'jquery',
    'config'
  ], function(
    Knockout,
    DishViewModel,
    _,
    jQuery,
    config
  ) {
'use strict';
var OrderViewModel = function() {
  var self = this;
  self.dishes = Knockout.observableArray();

  self.totalPrice = Knockout.computed(function() {
    return self.dishes().reduce(function(sum, dish) {
      return sum + (dish.price() * dish.amount());
    }, 0);
  });

  self.addDish = function(name, rest, amount, price) {
    var dish;
    if (name instanceof DishViewModel) {
      dish = name;
    }
    else {
      dish = _.find(self.dishes(), DishViewModel.filter.bind(null, name, rest));
    }
    if (dish) {
      dish.add(amount || 1);
    }
    else {
      self.dishes.push(new DishViewModel(name, rest, amount || 1, price));
    }
  };

  self.removeDish = function(dish) {
    if (!dish.minus().amount()) {
      self.dishes.remove(dish);
    }
  };

  self.save = function(uid) {
    return saveTo(config.uri.ORDER, uid);
  };

  self.saveDefault = function(uid) {
    return saveTo(config.uri.DEFAULT, uid);
  };

  self.toJSON = function() {
    return {
      'order': self.dishes().map(function(dish) {
        return dish.toJSON();
      })
    };
  };

  var saveTo = function(url, uid) {
    var defer = jQuery.Deferred();
    if (!self.dishes().length) {
      defer.reject(self, 'no dish');
      return defer;
    }
    var data = self.toJSON();
    data.id = uid;
    jQuery.post(url, { json: JSON.stringify(data)}).then(function() {
      defer.resolve(self);
    }, function(jqXHR) {
      if (jqXHR.status === 403) {
        defer.reject(self, 'overtime');
      }
      else {
        defer.reject(self, 'error');
      }
    });
    return defer;
  };
};

return OrderViewModel;

});