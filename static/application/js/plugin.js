(function ($, MODULE_CONFIG, MODULE_OPTION_CONFIG) {
  'use strict';
  $.fn.plugin = function () {
    return this.each(function () {
      var self = $(this);
      var opts = self.attr('data-option') || self.attr('data-plugin-option');
      var plugin = self.attr('data-plugin');
      if (self[plugin] && opts) {
        self[plugin].apply(self, getOpts(opts, plugin));
      } else {
        lazyload.load(MODULE_CONFIG[plugin]).then(function () {
          opts && self[plugin].apply(self, getOpts(opts, plugin));
          self[plugin] && self[plugin].init && self[plugin].init();
          window[plugin] && window[plugin].init && window[plugin].init();
        });
      }
      self.removeAttr('data-plugin').removeAttr('data-option');
    });

    function getOpts(opts, plugin) {
      var options = opts && eval('[' + opts + ']');
      if (options && $.isPlainObject(options[0])) {
        options[0] = $.extend({}, MODULE_OPTION_CONFIG[plugin], options[0]);
      }
      return options;
    }
  }
})(jQuery, MODULE_CONFIG, MODULE_OPTION_CONFIG);
