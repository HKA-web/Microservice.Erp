(function($, screenfull) {
  'use strict';
  $(document).on('click', '[data-toggle=\'fullscreen\']', function(e) {
    e.preventDefault();
    if (screenfull.enabled) {
      screenfull.toggle($('body')[0]);
    }
  });

  function fullscreenchange() {
    if (screenfull.isFullscreen) {
      $('body').addClass('is-fullscreen');
      $('[data-toggle=\'fullscreen\']').addClass('active');
      localStorage.setItem('fullscreen', true);
    } else {
      $('body').removeClass('is-fullscreen');
      $('[data-toggle=\'fullscreen\']').removeClass('active');
      localStorage.setItem('fullscreen', false);
    }
  }

  screenfull.on('change', fullscreenchange);
})(jQuery, screenfull);
