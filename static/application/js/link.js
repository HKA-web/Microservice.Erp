(function (ERPro) {
  'use strict';
  ERPro(function () {
    ERPro(document).on('click', 'a', function (e) {
      var anchor = ERPro(this);
      if (anchor.hasAttr('target')) {
        var data = {}
        if (ERPro.lo.includes([
          'post',
          'get',
          'delete',
          'frame',
          'iframe',
          'tab',
          'dialog',
          'window',
          'popup',
          'confirm',
        ], anchor.attr('target'))) {
          e.preventDefault();
          switch (anchor.attr('target')) {
            case 'frame':
            case 'iframe':
            case 'tab': {
              data = ERPro.lo.merge({}, {
                menu_id: anchor.hasAttr('id')
                  ? anchor.attr('id')
                  : ERPro.md5(anchor.attr('href')),
                menu_name: anchor.children().length
                  ? anchor.hasAttr('rel')
                    ? anchor.attr('rel')
                    : ERPro.lo.truncate(ERPro.lo.startCase(ERPro.common.toLocation(anchor.attr('href')).hostname), {length: 20})
                  : anchor.html(),
                action: anchor.attr('href'),
              });
              ERPro.each(anchor.dataSubset('config'), function (key, value) {
                data = ERPro.lo.merge(data, {[key]: value});
              });
              ERPro.util.tab.open(data)
              break;
            }
            case 'dialog':
            case 'window':
            case 'popup': {
              data = ERPro.lo.merge({}, {
                id: anchor.hasAttr('id')
                  ? anchor.attr('id')
                  : ERPro.md5(anchor.attr('href')),
                name: anchor.children().length
                  ? anchor.hasAttr('rel')
                    ? anchor.attr('rel')
                    : ERPro.lo.truncate(ERPro.lo.startCase(ERPro.common.toLocation(anchor.attr('href')).hostname), {length: 20})
                  : anchor.html(),
                action: anchor.attr('href'),
                config: {},
              });
              ERPro.each(anchor.dataSubset('config'), function (key, value) {
                data.config = ERPro.lo.merge(data.config, {[key]: value});
              });
              ERPro.util.dialog.open(data);
              break
            }
            case 'post':
            case 'get': {
              ERPro.ajax({
                url: anchor.attr('href'),
                data: anchor.dataSubset('data'),
                dataType: 'json',
                type: anchor.attr('target').toUpperCase(),
                success: function (data, textStatus, jqXHR) {
                  ERPro.util.toast.create(
                      gettext(ERPro.common.ucWord(jqXHR.statusText)),
                      gettext(data.message),
                      ERPro.util.toast.icon.Success,
                      function() {
                          if (anchor.hasClass('reload')) {
                              if (data.next) {
                                  window.location = data.next;
                              } else {
                                  window.location.reload();
                              }
                          }
                      }
                  );
                }
              });
              break
            }
            case 'confirm': {
              data = ERPro.lo.merge({}, {
                config: {
                  title: anchor.children().length
                    ? anchor.hasAttr('rel')
                      ? anchor.attr('rel')
                      : ERPro.lo.truncate(ERPro.lo.startCase(ERPro.common.toLocation(anchor.attr('href')).hostname), {length: 20})
                    : anchor.html(),
                  buttons: [],
                },
              });
              ERPro.each(anchor.dataSubset('config'), function (key, value) {
                data.config = ERPro.lo.merge(data.config, {[key]: value});
              });
              var buttons = []
              ERPro.each(anchor.dataSubset('buttons'), function (key, value) {
                buttons.push({
                  stylingMode: 'outlined',
                  text: value,
                  onClick: function (e) {
                    return {
                      key: key,
                      text: e.component.option('text'),
                    }
                  }
                })
              });
              data.config = ERPro.lo.merge(data.config, {buttons: buttons});
              var dialog = DevExpress.ui.dialog.custom(data.config);
              dialog.show()
                .done(function (click) {
                  var callback = eval(anchor.data('callback'))
                  if (typeof callback == 'function') {
                    callback(click);
                  }
                });
              if (anchor.hasAttr('data-timeout')) {
                setTimeout(function () {
                  dialog.hide()
                }, anchor.data('timeout'));
              }
              break;
            }
          }
        } else if (ERPro.lo.includes([
          '_blank',
          '_parent',
          '_self',
          '_top'
        ], anchor.attr('target'))) {} else {
          if (ERPro(anchor.attr('target')).length) {
            if (ERPro(anchor.attr('target')).is('iframe')) {
              if (ERPro(anchor.attr('target')).attr('src') !== anchor.attr('href')) {
                e.preventDefault();
                ERPro(anchor.attr('target')).attr('src', anchor.attr('href'));
              }
            } else if (ERPro(anchor.attr('target')).is('img')) {
              if (ERPro(anchor.attr('target')).attr('src') !== anchor.attr('href')) {
                e.preventDefault();
                ERPro(anchor.attr('target')).attr('src', anchor.attr('href'));
              }
            } else {
              if (ERPro(anchor.attr('target')).length) {
                e.preventDefault();
                ERPro(anchor.attr('target')).empty().load(anchor.attr('href'));
              }
            }
          }
        }
      }
    });
  });
})(jQuery);
