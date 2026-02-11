(function(ERPro) {
  'use strict';
  ERPro(document)
    .ajaxSend(function(event, jqXHR, settings, exception) {
      if (settings.headers) {
        if (!settings.headers.AspNetData) {
          ERPro.util.loader.show({
            message: false,
            showPane: false,
          });
        }
      } else {
        ERPro.util.loader.show({
          message: false,
          showPane: false,
        });
      }
    })
    .ajaxSuccess(function(event, jqXHR, settings, exception) {
      if (settings.headers) {
        if (!settings.headers.AspNetData) {
          ERPro.util.loader.hide();
        }
      } else {
        ERPro.util.loader.hide();
      }
    })
    .ajaxError(function(event, jqXHR, settings, exception) {
      var html = ERPro.parseHTML(jqXHR.responseText);
      if (debug) {
        console.log({ event: event, jqXHR: jqXHR, settings: settings, exception: exception });
      }
      if (ERPro(html).filter('meta[name=address]').length) {
        ERPro.util.toast.create(
            gettext('Redirect'),
            gettext('Page will redirect'),
            ERPro.util.toast.icon.Info,
            function() {
                window.top.location.reload();
            },
          );
      } else {
        if (settings.headers) {
          if (!settings.headers.AspNetData) {
            ERPro.util.loader.hide();
          }
        } else {
          settings.headers = {};
          ERPro.util.loader.hide();
        }
        if (!settings.headers.PreventError) {
          if (!jqXHR.responseJSON) {
            try {
              jqXHR.responseJSON = JSON.parse(jqXHR.responseText);
            } catch (e) {
            }
          }
          if (jqXHR.responseJSON) {
            if (jqXHR.responseJSON.error) {
              ERPro.util.toast.create(gettext(ERPro.common.ucWord(jqXHR.statusText)), gettext(jqXHR.responseJSON.error), ERPro.util.toast.icon.Error);
            }
            if (jqXHR.responseJSON.validation) {
              var messages = [];
              ERPro.each(jqXHR.responseJSON.validation, function(key, value) {
                messages.push(ERPro.common.sprintf('<b>%s</b>: <i>%s</i>', gettext(ERPro.common.ucWord(ERPro.common.onlyAlphanumeric(key, ' '))), gettext(value.join(', '))));
              });
              if (messages.length > 0) {
                ERPro.util.toast.create(jqXHR.responseJSON.error, messages, ERPro.util.toast.icon.Error);
              }
            }
            if (!ERPro.lo.some(ERPro.lo.intersection(['error', 'validation'], ERPro.lo.keys(jqXHR.responseJSON)))) {
              var messages = [];
              ERPro.each(jqXHR.responseJSON, function(key, value) {
                if (!Array.isArray(value)) {
                  value = [value];
                }
                messages.push(ERPro.common.sprintf('<i>%s</i>', gettext(value.join(', '))));
              });
              ERPro.util.toast.create(gettext(ERPro.common.ucWord(jqXHR.statusText)), messages, ERPro.util.toast.icon.Error);
            }
          } else {
            ERPro.util.toast.create(gettext(ERPro.common.ucWord(jqXHR.statusText)), gettext(ERPro(html).filter('title').text()), ERPro.util.toast.icon.Error);
            switch (jqXHR.status) {
              case 400: {
                break;
              }
              case 403: {
                break;
              }
              case 404: {
                break;
              }
              case 500: {
                if (ERPro(html).find('.exception_value').length) {
                  ERPro.util.toast.create(gettext(ERPro.common.ucWord(jqXHR.statusText)), gettext(ERPro(html).find('.exception_value').text()), ERPro.util.toast.icon.Error);
                }
                break;
              }
            }
          }
        }
      }
    });
})(jQuery);
