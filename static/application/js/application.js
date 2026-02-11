ERPro = jQuery || $ || {};
ERPro.fn.hasAttr = function(name) {
  return this.attr(name) !== undefined;
};
ERPro.fn.hasAnyClass = function() {
  var classes = arguments[0].split(' ');
  for (var loop = 0; loop < classes.length; loop++) {
    if (this.hasClass(classes[loop])) {
      return true;
    }
  }
  return false;
};
JSON.verify = function(s) {
  try {
    JSON.parse(s);
    return true;
  } catch (e) {
    return false;
  }
};
Audio.prototype.play = (function(play) {
  return function() {
    var audio = this,
      args = arguments,
      promise = play.apply(audio, args);
    if (promise !== undefined) {
      promise.catch(function(_) {
      });
    }
  };
})(Audio.prototype.play);
(function(ERPro) {
  'use strict';
  if (!!navigator.userAgent.match(/MSIE/i) || !!navigator.userAgent.match(/Trident.*rv:11\./)) {
    ERPro('body').addClass('ie');
  }
  var useragent = window['navigator']['userAgent'] || window['navigator']['vendor'] || window['opera'];
  if ((/iPhone|iPod|iPad|Silk|Android|BlackBerry|Opera Mini|IEMobile/).test(useragent)) {
    ERPro('body').addClass('touch');
  }
  if ((/iPhone|iPod|iPad/).test(useragent)) {
    ERPro(document, '.modal, .aside').on('shown.bs.modal', function(e) {
      var backdrop = ERPro('.modal-backdrop');
      ERPro(e.target).after(ERPro(backdrop));
    });
  }
  ERPro(window).on('resize', function() {
    var width = ERPro(window).width(), large = 1200, medium = 991, small = 768;
    if (width > large) {
      ERPro('.aside-lg').modal('hide');
    }
    if (width > medium) {
      ERPro('.mainaside').modal('hide');
      ERPro('.aside-md, .aside-sm').modal('hide');
    }
    if (width > small) {
      ERPro('.aside-sm').modal('hide');
    }
    if (width >= large) {
      ERPro('.subaside').removeClass('folded');
    }
    if (width >= medium) {
      ERPro('.subaside').removeClass('folded');
    }
    if (width <= small) {
      ERPro('.subaside').addClass('folded');
    }
  });
  ERPro(['body'].join('')).on('DOMMouseScroll mousewheel', function(event) {
    var header = ERPro('#header');
    if (event.originalEvent.detail > 0 || event.originalEvent.wheelDelta < 0) {
      header.removeClass('scroll-up').addClass('scroll-down');
    } else {
      header.removeClass('scroll-down').addClass('scroll-up');
    }
    if (ERPro(window).scrollTop() === 0) {
      header.removeClass('scroll-up scroll-down');
    }
  });
  ERPro(document).on('click', '[data-nav] a', function(e) {
    var active, li, lili;
    li = ERPro(this).parent();
    lili = li.parents('li');
    active = li.closest('[data-nav]').find('.active');
    lili.addClass('active');
    (ERPro(this).next().is('ul') && li.toggleClass('active') && e.preventDefault()) || li.addClass('active');
    active.not(lili).not(li).removeClass('active');
    if (ERPro(this).attr('href') && ERPro(this).attr('href') !== '#' && ERPro(this).attr('href') !== 'javascript:void(0)') {
      ERPro(document).trigger('Nav:changed');
    }
  });
  ERPro(document).on('click', '[data-toggle-class]', function(e) {
    var element = ERPro(this);
    var attribute = element.attr('data-toggle-class');
    var target = element.attr('data-toggle-class-target') || element.attr('data-target');
    var closest = element.attr('data-target-closest');
    var classes = (attribute && attribute.split(',')) || '',
      targets = (target && target.split(',')) || Array(element),
      key = 0;
    ERPro.each(classes, function(index, value) {
      var target = closest ? element.closest(targets[(targets.length === 1 ? 0 : key)]) : ERPro(targets[(targets.length === 1 ? 0 : key)]),
        current = target.attr('data-class'),
        theclass = classes[index];
      (current !== theclass) && target.removeClass(target.attr('data-class'));
      target.toggleClass(classes[index]);
      target.attr('data-class', theclass);
      key++;
    });
    element.toggleClass('active');
    element.attr('href') === '#' || element.attr('href') === 'javascript:void(0)' ? e.preventDefault() : '';
  });
  var url = window.location.pathname.split('/');
  if (url.length > 0) {
    url = url[url.length - 1];
  }
  ERPro('[data-nav] li.active').removeClass('active');
  ERPro('[data-nav] a').filter(function() {
    return url === ERPro(this).attr('href') && ERPro(this).attr('href') !== '#' && ERPro(this).attr('href') !== 'javascript:void(0)';
  }).parents('li')
    .addClass('active');
  window.hexToRGB = function(hex, alpha) {
    var red = parseInt(hex.slice(1, 3), 16),
      green = parseInt(hex.slice(3, 5), 16),
      blue = parseInt(hex.slice(5, 7), 16);
    return 'rgba(' + red + ', ' + green + ', ' + blue + ', ' + alpha + ')';
  };
  ERPro(document).on('click', '[data-toggle=\'reload\']', function(e) {
    e.preventDefault();
    ERPro.util.tab.reload();
  });
  ERPro(document).on('click', '[data-toggle=\'modal\']', function(e) {
    var element = ERPro(this);
    var target = element.attr('data-target');
    if (target.startsWith('parent:')) {
      var find = target.split(':');
      var modal = ERPro(find[find.length - 1], window.parent.document);
      if (modal.length) {
        modal.modal('show');
      }
    }
  });
  ERPro(function() {
    ERPro('div.inner').width(ERPro(window).width() - ERPro('div.outter').width() - .5);
    ERPro('div.scrollable').dxScrollView({
      scrollByContent: true,
      scrollByThumb: true,
      showScrollbar: 'onScroll',
      reachBottomText: gettext('Updating...'),
      height: ERPro('div.modulepanel', window.top.document).find('div.dx-multiview-item-container').height() - ERPro('div.navbar').outerWidth(),
    });
  });
  ERPro(window).on('resize', function() {
    ERPro('div.inner').width(ERPro(window).width() - ERPro('div.outter').width() - .5);
    ERPro('div.scrollable').dxScrollView('option', 'height', ERPro('div.modulepanel', window.top.document).find('div.dx-multiview-item-container').height() - ERPro('div.navbar').outerWidth());
  });
  ERPro(window).on('keydown', function(event) {
    if (event.keyCode === 116) {
      event.preventDefault();
      ERPro.util.toast.create(gettext('Warning'), interpolate(gettext('Disable %(key)s keyboard, Please reload manual'), event, true), ERPro.util.toast.icon.Warning);
      return false;
    }
  });
  ERPro.each(['show', 'hide', 'addClass', 'removeClass'], function() {
    var functions = ERPro.fn[this];
    ERPro.fn[this] = function() {
      var hidden = this.find(':hidden').add(this.filter(':hidden'));
      var visible = this.find(':visible').add(this.filter(':visible'));
      var result = functions.apply(this, arguments);
      hidden.filter(':visible').each(function() {
        ERPro(this).triggerHandler('show');
      });
      visible.filter(':hidden').each(function() {
        ERPro(this).triggerHandler('hide');
      });
      return result;
    };
  });
})(jQuery);
