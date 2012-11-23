define([
    'jquery',
    'knockout',
    'view-models/menu-view-model',
    'view-models/restaurants-view-model',
    'controllers/message-center',
    'view-models/order-view-model',
    'view-models/user-view-model',
    'view-models/alert-view-model',
    'bindings/delay-css',
    'underscore'
  ], function(
    jQuery,
    Knockout,
    MenuViewModel,
    RestaurantsViewModel,
    MessageCenter,
    OrderViewModel,
    UserViewModel,
    alert,
    BindingDelayCss,
    _
  ) {
'use strict';

// Data logic.
var rests = new RestaurantsViewModel();
var menu = new MenuViewModel();
var order = new OrderViewModel();
var userInfoModal = jQuery('#userinfo');

UserViewModel.nameAbsent.subscribe(function(value) {
  userInfoModal.modal(value ? 'show' : 'hide');
});

rests.on('change-menu', function(newURL) {
  menu.fetch(newURL);
});

menu.on('order', function(name, price) {
  order.addDish(name, rests.selectedRestName(), 1, price);
});

jQuery(document.body)
  .ajaxStart(function() {
    this.classList.add('loading');
  })
  .ajaxStop(function() {
    this.classList.remove('loading');
  })
  .tooltip({
    selector: 'a[rel=tooltip]',
    placement: 'bottom'
  });

var $search = jQuery('#search-dish');
var search = {
  addDish: function() {
    var dish;
    var name = $search.val();
    _.any(menu.menu(), function(group) {
      return (dish = _.find(group.dishes, function(dish) {
        return dish.name === name;
      }));
    });
    if (dish) {
      order.addDish(dish.name, rests.selectedRestName(), 1, dish.price);
      $search.val('').tooltip('hide');
    }
  }
};
$search.typeahead({
  source: function() {
    return menu.dishes();
  },
  updater: function(item) {
    $search.tooltip('show');
    return item;
  }
}).tooltip().on('blur', function() { $search.tooltip('hide'); });

// Take off!!
UserViewModel.fetch()
  .pipe(function() {
    return rests.fetch();
  },function() {
    bindingContext.needSignIn(true);
  }).
  done(function() {
    // bindingContext.needSignIn(true);
    bindingContext.loaded(true);
  });

// rests.fetch();


var bindingContext = {
  loaded: Knockout.observable(false),
  needSignIn: Knockout.observable(false),
  user: UserViewModel,
  menu: menu,
  rests: rests,
  alert: alert,
  search: search,
  order: Knockout.observable(order),
  newOrder: function() {
    this.order(order = new OrderViewModel());
  },
  makeOrder: function() {
    if (window.confirm('本单总计 ' + (order.totalPrice() / 100).toFixed(2) + '元，吃不了崔阿姨搞死你哦，确定要下单吗？')) {
      this.order().save().done(function() {
        alert.message('订单保存成功！');
        this.newOrder();
      }.bind(this)).fail(function(o, msg) {
        if (msg === 'no dish') {
          alert('淡定。。。还没点呢 -_-|||');
        }
        else {
          alert.message('订单保存失败，再试一次？');
        }
      });
    }
  },
  confirmSignout: function(data, e) {
    return window.confirm('真心不吃了么？');
  }
};
bindingContext.welcomeStatus = Knockout.computed(function() {
  return this.loaded() ? 'greeting' : this.needSignIn() ? 'signin' : 'loading';
}, bindingContext);

Knockout.applyBindings(bindingContext);

_.delay(function() {
  alert('5分钟了还没选好。。。你也和小明一样有选择恐惧症吗？');
}, 5 * 60 * 1000);

window.user = UserViewModel;
window.bc = bindingContext;
});