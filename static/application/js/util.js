(function(ERPro) {
  'use strict';
  ERPro.extend({
    lo: _,
    signals: function(name, callback) {
      window.top.ERPro(window.top.document).on(name, callback);
    },
    send: function(signal, data) {
      window.top.ERPro(window.top.document).trigger(signal, data);
    },
    common: {
      isUndefined: function(value) {
        return value === undefined;
      },
      isNull: function(value) {
        return value === null;
      },
      isBoolean: function(value) {
        return typeof value === 'boolean';
      },
      isObject: function(value) {
        return value === Object(value);
      },
      isArray: function(value) {
        return Array.isArray(value);
      },
      isDate: function(value) {
        return value instanceof Date;
      },
      isReactNativeBlob: function(value) {
        return (
          typeof new FormData().getParts === 'function' &&
          ERPro.common.isObject(value) &&
          !ERPro.common.isUndefined(value.uri)
        );
      },
      isBlob: function(value) {
        return (
          (ERPro.common.isObject(value) &&
            typeof value.size === 'number' &&
            typeof value.type === 'string' &&
            typeof value.slice === 'function') ||
          ERPro.common.isReactNativeBlob(value)
        );
      },
      isFile: function(value) {
        return (
          ERPro.common.isBlob(value) &&
          typeof value.name === 'string' &&
          (ERPro.common.isObject(value.lastModifiedDate) || typeof value.lastModified === 'number')
        );
      },
      ifUndefinedThenFalse: function(value) {
        return ERPro.common.isUndefined(value) ? false : value;
      },
      objectToForm: function(object, config, formData, prepare) {
        config = config || {};
        formData = formData || new FormData();
        config.indices = ERPro.common.ifUndefinedThenFalse(config.indices);
        config.nullsAsUndefineds = ERPro.common.ifUndefinedThenFalse(config.nullsAsUndefineds);
        config.booleansAsIntegers = ERPro.common.ifUndefinedThenFalse(config.booleansAsIntegers);
        config.allowEmptyArrays = ERPro.common.ifUndefinedThenFalse(config.allowEmptyArrays);
        config.noFilesWithArrayNotation = ERPro.common.ifUndefinedThenFalse(config.noFilesWithArrayNotation);
        config.dotsForObjectNotation = ERPro.common.ifUndefinedThenFalse(config.dotsForObjectNotation);
        if (ERPro.common.isUndefined(object)) {
          return formData;
        } else if (ERPro.common.isNull(object)) {
          if (!config.nullsAsUndefineds) {
            formData.append(prepare, '');
          }
        } else if (ERPro.common.isBoolean(object)) {
          if (config.booleansAsIntegers) {
            formData.append(prepare, object ? 1 : 0);
          } else {
            formData.append(prepare, object);
          }
        } else if (ERPro.common.isArray(object)) {
          if (object.length) {
            object.forEach((value, index) => {
              let key = prepare + '[' + (config.indices ? index : '') + ']';
              if (config.noFilesWithArrayNotation && ERPro.common.isFile(value)) {
                key = prepare;
              }
              ERPro.common.objectToForm(value, config, formData, key);
            });
          } else if (config.allowEmptyArrays) {
            formData.append(prepare + '[]', '');
          }
        } else if (ERPro.common.isDate(object)) {
          formData.append(prepare, object.toISOString());
        } else if (ERPro.common.isObject(object) && !ERPro.common.isBlob(object)) {
          Object.keys(object).forEach((prop) => {
            const value = object[prop];
            if (ERPro.common.isArray(value)) {
              while (prop.length > 2 && prop.lastIndexOf('[]') === prop.length - 2) {
                prop = prop.substring(0, prop.length - 2);
              }
            }
            const key = prepare
              ? config.dotsForObjectNotation
                ? prepare + '.' + prop
                : prepare + '[' + prop + ']'
              : prop;
            ERPro.common.objectToForm(value, config, formData, key);
          });
        } else {
          formData.append(prepare, object);
        }
        return formData;
      },
      isEmpty: function(value) {
        return typeof value === 'undefined' || value == null || this.trim(value) === '';
      },
      isNotEmpty: function(value) {
        return !ERPro.common.isEmpty(value);
      },
      nullToStr: function(value) {
        if (ERPro.common.isEmpty(value)) {
          return '-';
        }
        return value;
      },
      visible: function(value) {
        return ERPro.common.isEmpty(value) || value === true;
      },
      trim: function(value) {
        if (value == null) {
          return '';
        }
        return value.toString().replace(/(^\s*)|(\s*$)|\r|\n/g, '');
      },
      equals: function(string, that) {
        return string === that;
      },
      equalsIgnoreCase: function(string, that) {
        return String(string).toUpperCase() === String(that).toUpperCase();
      },
      split: function(string, separator, maxLength) {
        if (ERPro.common.isEmpty(string)) {
          return null;
        }
        var value = String(string).split(separator);
        return maxLength
          ? value.slice(0, maxLength - 1)
          : value;
      },
      sprintf: function(string) {
        var temporary = arguments, flag = true, loop = 1;
        string = string.replace(/%s/g, function() {
          var argument = temporary[loop++];
          if (typeof argument === 'undefined') {
            flag = false;
            return '';
          }
          return argument == null
            ? ''
            : argument;
        });
        return flag
          ? string
          : '';
      },
      dateFormat: function(date, format) {
        var that = this;
        if (that.isEmpty(date)) return '';
        if (!date) return;
        if (!format) format = 'yyyy-MM-dd';
        switch (typeof date) {
          case 'string':
            date = new Date(date.replace(/-/, '/'));
            break;
          case 'number':
            date = new Date(date);
            break;
        }
        if (!date instanceof Date) return;
        var dictionary = {
          'yyyy': date.getFullYear(),
          'M': date.getMonth() + 1,
          'd': date.getDate(),
          'H': date.getHours(),
          'm': date.getMinutes(),
          's': date.getSeconds(),
          'MM': ('' + (date.getMonth() + 101)).substr(1),
          'dd': ('' + (date.getDate() + 100)).substr(1),
          'HH': ('' + (date.getHours() + 100)).substr(1),
          'mm': ('' + (date.getMinutes() + 100)).substr(1),
          'ss': ('' + (date.getSeconds() + 100)).substr(1),
        };
        return format.replace(/(yyyy|MM?|dd?|HH?|ss?|mm?)/g,
          function() {
            return dictionary[arguments[0]];
          });
      },
      getItemField: function(item, field) {
        var value = item;
        if (typeof field !== 'string' || item.hasOwnProperty(field)) {
          return item[field];
        }
        var props = field.split('.');
        for (var p in props) {
          value = value && value[props[p]];
        }
        return value;
      },
      random: function(min, max) {
        return Math.floor((Math.random() * max) + min);
      },
      startWith: function(value, start) {
        var regexp = new RegExp('^' + start);
        return regexp.test(value);
      },
      endWith: function(value, end) {
        var regexp = new RegExp(end + '$');
        return regexp.test(value);
      },
      uniqueFunction: function(array) {
        var result = [];
        var hashObject = {};
        for (var loop = 0; loop < array.length; loop++) {
          if (!hashObject[array[loop]]) {
            hashObject[array[loop]] = true;
            result.push(array[loop]);
          }
        }
        return result;
      },
      join: function(array, separator) {
        if (ERPro.common.isEmpty(array)) {
          return null;
        }
        return array.join(separator);
      },
      formToJSON: function(formId) {
        var json = {};
        ERPro.each(ERPro(['#', formId].join('')).serializeArray(), function(index, field) {
          if (json[field.name]) {
            json[field.name] += (',' + field.value);
          } else {
            json[field.name] = field.value;
          }
        });
        return json;
      },
      dataToSelect: function(data, value, name) {
        var actions = [];
        actions.push(ERPro.common.sprintf('<select class=\'form-control\' name=\'%s\'>', name));
        ERPro.each(data, function(index, row) {
          actions.push(ERPro.common.sprintf('<option value=\'%s\'', row.value));
          if (row.value === ('' + value)) {
            actions.push(' selected');
          }
          actions.push(ERPro.common.sprintf('>%s</option>', row.label));
        });
        actions.push('</select>');
        return actions.join('');
      },
      getLength: function(object) {
        var count = 0;
        for (var row in object) {
          if (object.hasOwnProperty(row)) {
            count++;
          }
        }
        return count;
      },
      isMobile: function() {
        return navigator.userAgent.match(/(Android|iPhone|SymbianOS|Windows Phone|iPad|iPod)/i);
      },
      numericValid: function(value) {
        var patten = new RegExp(/^[0-9]+$/);
        return patten.test(value);
      },
      alphabetValid: function(value) {
        var patten = new RegExp(/^[a-zA-Z]+$/);
        return patten.test(value);
      },
      alphabetNumericValid: function(value) {
        var patten = new RegExp(/^(?=.*[a-zA-Z]+)(?=.*[0-9]+)[a-zA-Z0-9]+$/);
        return patten.test(value);
      },
      characterValid: function(value) {
        var patten = new RegExp(/^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#\$%\^&\*\(\)\-=_\+])[A-Za-z\d~!@#\$%\^&\*\(\)\-=_\+]{6,}$/);
        return patten.test(value);
      },
      ucFirst: function(value) {
        return this.trim(value).charAt(0).toUpperCase() + this.trim(value).toLowerCase().slice(1);
      },
      ucWord: function(value) {
        return this.trim(value).toLowerCase().replace(/(?<= )[^\s]|^./g, function(s) {
          return s.toUpperCase();
        });
      },
      onlyAlphanumeric: function(value, replacer) {
        return value.replace(/[^0-9a-z]/gi, replacer ? replacer : '');
      },
      toLocation: function(url) {
        return (ERPro('<a/>', { href: url }))[0];
      },
      delay: function(callback, ms) {
        var timer = 0;
        return function() {
          var context = this, args = arguments;
          clearTimeout(timer);
          timer = setTimeout(function() {
            callback.apply(context, args);
          }, ms || 0);
        };
      },
    },
    util: {
      toast: {
        icon: {
          Info: TOAST_STATUS.INFO,
          Warning: TOAST_STATUS.WARNING,
          Error: TOAST_STATUS.DANGER,
          Success: TOAST_STATUS.SUCCESS,
        },
        position: {
          TopLeft: TOAST_PLACEMENT.TOP_LEFT,
          TopCenter: TOAST_PLACEMENT.TOP_CENTER,
          TopRight: TOAST_PLACEMENT.TOP_RIGHT,
          MiddleLeft: TOAST_PLACEMENT.MIDDLE_LEFT,
          MiddleCenter: TOAST_PLACEMENT.MIDDLE_CENTER,
          MiddleRight: TOAST_PLACEMENT.MIDDLE_RIGHT,
          BottomLeft: TOAST_PLACEMENT.BOTTOM_LEFT,
          BottomCenter: TOAST_PLACEMENT.BOTTOM_CENTER,
          BottomRight: TOAST_PLACEMENT.BOTTOM_RIGHT,
        },
        create: function(title, message, status = TOAST_STATUS.INFO, onHidden, timeout = 5000, pauseOnHover = true, position = TOAST_PLACEMENT.TOP_RIGHT) {
          Toast.setPlacement(position);
          if (ERPro.common.isMobile() && !(DevExpress.devices.current().deviceType.match(/(tablet|desktop)/i))) {
            Toast.setPlacement(TOAST_PLACEMENT.TOP_CENTER);
          }
          if (window.top !== window.self) {
            window.top.ERPro.util.toast.create(title, message, status, onHidden, timeout, pauseOnHover, position);
          } else {
            Toast.create({
              title: title,
              message: message,
              status: status,
              timeout: timeout,
              pauseDelayOnHover: pauseOnHover,
              onHidden: typeof onHidden === 'function' ? onHidden : function(e) {
              },
            });
          }
        },
      },
      loader: {
        show: function(data, of) {
          var config = ERPro.lo.merge({
            wrapperAttr: {
              class: 'pageloadpanel',
            },
            width: 250,
            height: 250,
            shadingColor: 'rgba(0, 0, 0, 0)',
            visible: false,
            hideOnOutsideClick: false,
            onContentReady: function(e) {
              e.component.content().addClass('shadown');
              if (typeof data === 'object' && 'shadow' in data && !data.shadow) {
                e.component.content().removeClass('shadown');
              }
              if (typeof data === 'object' && data.message && !ERPro.common.isEmpty(data.message)) {
                e.component.content().find('div.dx-loadpanel-message').empty().html(`<b>${data.message}</b><br/>${gettext('Processing')}`);
              }
            },
            onShown: function() {
            },
            onHidden: function() {
            },
          }, typeof data === 'object' ? data : { message: data });
          if (ERPro.common.isEmpty(config.message)) {
            config = ERPro.lo.merge(config, { message: false });
          }
          if (ERPro.common.isEmpty(config.of)) {
            config = ERPro.lo.merge(config, {
              of: typeof of === 'undefined' ? 'body' : of,
            });
          }
          if (ERPro.common.isEmpty(config.showIndicator)) {
            config = ERPro.lo.merge(config, { showIndicator: true });
          }
          if (ERPro.common.isEmpty(config.showPane)) {
            config = ERPro.lo.merge(config, { showPane: true });
          }
          if (ERPro.common.isEmpty(config.shading)) {
            config = ERPro.lo.merge(config, { shading: true });
          }
          if (!ERPro('div#loader').length) {
            ERPro('<div/>', {
              id: 'loader',
              appendTo: 'body',
            });
          }
          ERPro('div#loader').dxLoadPanel(ERPro.lo.merge(config, {
            position: {
              of: config.of,
            },
            showIndicator: config.showIndicator,
            showPane: config.showPane,
            shading: config.shading,
          })).dxLoadPanel('instance').show();
          if (config.message && !ERPro.common.isEmpty(config.message)) {
            ERPro('div#loader').dxLoadPanel('instance')
              .content()
              .find('div.dx-loadpanel-message')
              .empty()
              .html(`<b>${config.message}</b><br/>${gettext('Processing')}`);
          }
          if ('shadow' in config && !config.shadow) {
            ERPro('div#loader').dxLoadPanel('instance')
              .content()
              .removeClass('shadown');
          }
        },
        hide: function() {
          setTimeout(function() {
            if (ERPro('div#loader').length) {
              ERPro('div#loader').dxLoadPanel('instance').hide();
              ERPro('div#loader').remove();
            }
          }, 500);
        },
      },
      page: {
        title: function(title) {
          window.top.document.title = title.includes(systemname) ? title : [title, systemname].join(' : ');
        },
        url: function(target, url) {
          if (target && url) {
            window.top.location = [window.top.location.protocol, '//', [window.top.location.host, window.top.location.pathname, '#/'].join('/').replaceAll('//', '/'), target, ':/', url.startsWith('http') ? url : url.replace(/^\/?|\/?$/, '').replaceAll('#', '')].join('');
          } else {
            window.top.history.replaceState({}, document.title, window.top.location.href.split('#')[0]);
          }
        },
        address: function() {
          return ERPro('meta[name=address]').attr('content');
        },
      },
      tab: {
        datasource: function() {
          if (ERPro('div.modulepanel').length) {
            return {
              data: ERPro('div.modulepanel').dxTabPanel('option', 'dataSource'),
              selected: ERPro('div.modulepanel').dxTabPanel('option', 'selectedIndex'),
            };
          } else {
            if (window === window.parent) {
              ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not get datasource tab'), ERPro.util.toast.icon.Error);
              return {};
            } else {
              return window.parent.ERPro.util.tab.datasource();
            }
          }
        },
        open: function(data) {
          if (ERPro('div.modulepanel').length) {
            var datasource = ERPro.util.tab.datasource().data;
            var index = ERPro.lo.findIndex(datasource, function(row) {
              return row.menu_id === data.menu_id;
            });
            if (index > -1) {
              ERPro('div.modulepanel').dxTabPanel('option', 'selectedIndex', index);
            } else {
              ERPro.util.loader.show({
                message: false,
                showPane: false,
              }, 'div.dx-multiview-wrapper');
              datasource.push(data);
              ERPro('div.modulepanel').dxTabPanel({
                dataSource: datasource,
                selectedIndex: datasource.length - 1,
              });
            }
            ERPro.util.page.url('tab', data.action);
            var title = ERPro(['iframe', data.menu_id].join('#')).contents().find('title').html();
            ERPro.util.page.title(title ? title : data.menu_name);
          } else {
            if (window === window.parent) {
              ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not open tab'), ERPro.util.toast.icon.Error);
            } else {
              window.parent.ERPro.util.tab.open(data);
            }
          }
        },
        reload: function(data) {
          var datasource = ERPro.util.tab.datasource();
          var selected = data ? data : datasource.data[datasource.selected];
          if (ERPro('div.modulepanel').length) {
            var iframe = ERPro(['iframe', selected.menu_id].join('#'));
            if (iframe.hasAttr('noreload')) {
              ERPro.util.toast.create(gettext('Warning'), interpolate(gettext('Module %(menu_name)s contain dialog open, Please close first'), selected, true), ERPro.util.toast.icon.Warning);
            } else {
              ERPro.util.loader.show({
                message: false,
                showPane: false,
              }, 'div.dx-multiview-wrapper');
              iframe.attr('src', iframe.attr('src'));
              iframe.on('load', function() {
                setTimeout(function() {
                  ERPro.util.loader.hide();
                }, 2000);
              });
            }
          } else {
            if (window === window.parent) {
              ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not reload tab'), ERPro.util.toast.icon.Error);
            } else {
              window.parent.ERPro.util.tab.reload(selected);
            }
          }
        },
        close: function(data) {
          if (ERPro('div.modulepanel').length) {
            var datasource = ERPro.util.tab.datasource().data;
            var index = datasource.indexOf(data);
            ERPro('div.modulepanel').dxTabPanel('instance')
              .element()
              .find('iframe#' + datasource[index].menu_id)
              .removeAttr('src');
            datasource.splice(index, 1);
            ERPro('div.modulepanel').dxTabPanel('option', 'dataSource', datasource);
            if (index >= datasource.length && index > 0) {
              ERPro('div.modulepanel').dxTabPanel('option', 'selectedIndex', index - 1);
            }
            var selected = ERPro.util.tab.datasource().data[ERPro.util.tab.datasource().selected];
            if (selected) {
              ERPro.util.page.url('tab', selected.action);
              ERPro.util.page.title(selected.menu_name);
            } else {
              ERPro.util.page.url();
            }
          } else {
            if (window === window.parent) {
              ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not close tab'), ERPro.util.toast.icon.Error);
            } else {
              window.parent.ERPro.util.tab.close(data);
            }
          }
        },
      },
      dialog: {
        open: function(data) {
          data = ERPro.lo.merge(data, {
            id: data.id
              ? data.id
              : ERPro.md5(data.action),
          });
          var config = ERPro.lo.merge(data.config ? data.config : {}, {
            dragEnabled: true,
            showCloseButton: true,
            hideOnOutsideClick: false,
            resizeEnabled: true,
            focusStateEnabled: false,
            toolbarItems: [{
              widget: 'dxButton',
              location: 'after',
              options: {
                stylingMode: 'text',
                icon: 'fullscreen',
                elementAttr: {
                  id: 'fullscreen',
                },
                onClick: function(e) {
                  ERPro.util.dialog.fullscreen(data);
                },
              },
            }],
            onOptionChanged: function(e) {
              if (e.name === 'fullScreen') {
                if (!e.value) {
                  ERPro(['div.dialog', data.id].join('#')).dxPopup('instance')
                    .content()
                    .parent()
                    .parent()
                    .find('div.dx-popup-fullscreen')
                    .removeClass('border-0');
                }
              }
            },
            onShown: function(e) {
              e.component.content().parent().parent().addClass('dialog');
            },
            onHidden: function(e) {
              e.component.dispose();
              ERPro(['div.dialog', data.id].join('#')).remove();
            },
          });
          if (ERPro.common.isEmpty(config.width)) {
            config = ERPro.lo.merge(config, { width: ERPro(window).width() > 800 ? 800 : ERPro(window).width() - 50 });
          }
          if (ERPro.common.isEmpty(config.height)) {
            config = ERPro.lo.merge(config, { height: (ERPro(window).height() - 50) });
          }
          var original = {
            width: config.width,
            height: config.height,
          };
          if (config.width > (ERPro(window).width() - 50)) {
            config = ERPro.lo.merge(config, { width: (ERPro(window).width() - 50) });
          }
          if (config.height > (ERPro(window).height() - 50)) {
            config = ERPro.lo.merge(config, { height: (ERPro(window).height() - 50) });
          }
          if (ERPro.common.isMobile() && !(DevExpress.devices.current().deviceType.match(/(tablet|desktop)/i))) {
            config = ERPro.lo.merge(config, { fullScreen: true });
          }
          if (ERPro.common.isEmpty(data.name)) {
            data = ERPro.lo.merge(data, { name: 'Action' });
          }
          if (ERPro.common.isEmpty(data.action)) {
            data = ERPro.lo.merge(data, { action: '404.html' });
          }
          config = ERPro.lo.merge(config, {
            original: original,
            contentTemplate: function() {
              return ERPro('<iframe/>', {
                class: 'd-flex flex h-100 w-100 block m-0',
                id: data.id,
                onload: function(e) {
                  setTimeout(function() {
                    ERPro.util.loader.hide();
                  }, 2000);
                },
                onerror: function(e) {
                  console.log(e);
                },
              });
            }, onContentReady: function(e) {
              e.component.content().addClass('p-0');
            },
          });
          if (!ERPro(['div.dialog', data.id].join('#')).length) {
            ERPro('<div/>', {
              class: 'dialog',
              id: data.id,
              appendTo: 'body',
            });
            ERPro(['div.dialog', data.id].join('#')).attr('address', data.action);
          }
          ERPro(['div.dialog', data.id].join('#')).dxPopup(config).dxPopup('instance').show();
          ERPro(['div.dialog', data.id].join('#')).dxPopup('instance')
            .on('shown', function(e) {
              e.component.content().find('iframe#' + data.id).attr('src', data.action); /* for: fix iframe load multiple canceled */
              var iframe = ERPro('iframe[src=\'' + ERPro.util.page.address() + '\']', window.parent.document);
              if (iframe.length) {
                iframe.attr('noreload', true);
              }
              ERPro.util.loader.show({
                message: false,
                showPane: false,
              });
              if (ERPro.common.isEmpty(data.title)) {
                var title = ERPro(['iframe', data.id].join('#')).contents().find('title').html();
                ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'title', title ? title : data.name);
              }
              ERPro.util.page.title(ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'title'));
            })
            .on('hiding', function(e) {
               e.component.content().find('iframe#' + data.id).removeAttr('src'); /* for: fix iframe load multiple canceled */
            })
            .on('hidden', function(e) {
              var iframe = ERPro('iframe[src=\'' + ERPro.util.page.address() + '\']', window.parent.document);
              if (iframe.length) {
                iframe.removeAttr('noreload');
              }
              var datasource = ERPro.util.tab.datasource();
              if (datasource.selected) {
                var selected = datasource.data[datasource.selected];
                ERPro.util.page.url('tab', selected.action);
                ERPro.util.page.title(selected.menu_name);
              }
            });
          ERPro.util.page.url('dialog', data.action);
          ERPro(['div.dialog', data.id].join('#')).dxPopup('instance')
            .content()
            .parent()
            .on('click', 'div.dx-popup-title', function(e) {
              if (ERPro.common.isEmpty(data.title)) {
                var title = ERPro(['iframe', data.id].join('#')).contents().find('title').html();
                ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'title', title ? title : data.name);
              }
              ERPro.util.page.url('dialog', data.action);
              ERPro.util.page.title(ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'title'));
            }).on('dblclick', 'div.dx-popup-title', function(e) {
            ERPro.util.dialog.fullscreen(data);
          });
          ERPro(window).on('resize', function() {
            ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'width', (config.width > (ERPro(window).width() - 50) ? ERPro(window).width() - 50 : config.original.width));
            ERPro(['div.dialog', data.id].join('#')).dxPopup('option', 'height', (config.height > (ERPro(window).height() - 50) ? ERPro(window).height() - 50 : config.original.height));
          });
        },
        fullscreen: function(data) {
          if (ERPro(['div.dialog', data.id].join('#')).dxPopup('instance')
            .content()
            .parent()
            .parent()
            .find('div.dx-popup-fullscreen').length) {
            ERPro(['div.dialog', data.id].join('#')).dxPopup({
              fullScreen: false,
              showCloseButton: true,
              position: {
                my: 'center',
                at: 'center',
                of: window,
              },
            });
            ERPro('div#fullscreen').dxButton('option', 'icon', 'fullscreen');
          } else {
            ERPro(['div.dialog', data.id].join('#')).dxPopup({
              fullScreen: true,
              showCloseButton: false,
            });
            ERPro(['div.dialog', data.id].join('#')).dxPopup('instance')
              .content()
              .parent()
              .parent()
              .find('div.dx-popup-fullscreen')
              .addClass('border-0');
            ERPro('div#fullscreen').dxButton('option', 'icon', 'dx-icon-fullscreen rotate-45');
          }
        },
        instance: function(address) {
          if (address) {
            if (ERPro('div.dialog[address=\'' + address + '\']').length) {
              return ERPro('div.dialog[address=\'' + address + '\']').dxPopup('instance');
            } else {
              if (window === window.parent) {
                ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not get instance dialog'), ERPro.util.toast.icon.Error);
              } else {
                return window.parent.ERPro.util.dialog.instance(address);
              }
            }
          } else {
            return ERPro.util.dialog.instance(ERPro.util.page.address());
          }
        },
        close: function(address) {
          if (address) {
            if (ERPro('div.dialog[address=\'' + address + '\']').length) {
              ERPro('div.dialog[address=\'' + address + '\']').dxPopup('hide');
            } else {
              if (window === window.parent) {
                ERPro.util.toast.create(gettext('Error'), gettext('Maximum top window, Can not close dialog'), ERPro.util.toast.icon.Error);
              } else {
                window.parent.ERPro.util.dialog.close(address);
              }
            }
          } else {
            ERPro.util.dialog.close(ERPro.util.page.address());
          }
        },
      },
      ws: function(url, protocols, options) {
        var socket = new ReconnectingWebSocket(
          url ? url : `ws://${window.location.host}/ws/subscribe/`,
          protocols ? protocols : [],
          ERPro.lo.merge({
            debug: true,
            msgpack: true,
            indicator: true,
          }, options),
        );
        if (socket._options.indicator) {
          var events = {
            'CREATED': 'fa-chevrons-down faa-bounce',
            'UPDATED': 'fa-arrow-down-to-arc faa-bounce',
            'DELETED': 'fa-chevrons-right faa-horizontal',
          };

          function message(event) {
            ERPro('span > i.websocket', window.top.document)
              .removeClass(ERPro.lo.values(events).join(' '))
              .removeClass('fa-chevrons-down faa-bounce fa-sun-bright fa-bolt-slash fa-bug faa-burst faa-slow faa-fast text-warning text-danger text-success')
              .addClass('animated faa-fast text-success')
              .addClass(events[event]);
            setTimeout(function() {
              ERPro('span > i.websocket', window.top.document)
                .removeClass(ERPro.lo.values(events).join(' '))
                .removeClass('fa-chevrons-down faa-bounce fa-sun-bright fa-bolt-slash fa-bug faa-burst faa-slow faa-fast text-warning text-danger text-success')
                .addClass('fa-sun-bright faa-burst animated faa-slow text-success');
            }, 2000);
          }

          socket.addEventListener('open', function(e) {
            ERPro('span > i.websocket', window.top.document)
              .removeClass(ERPro.lo.values(events).join(' '))
              .removeClass('fa-chevrons-down faa-bounce fa-sun-bright fa-bolt-slash fa-bug faa-burst faa-slow faa-fast text-warning text-danger text-success')
              .addClass('fa-sun-bright faa-burst animated faa-slow text-success');
          });
          socket.addEventListener('close', function(e) {
            ERPro('span > i.websocket', window.top.document)
              .removeClass(ERPro.lo.values(events).join(' '))
              .removeClass('fa-chevrons-down faa-bounce fa-sun-bright fa-bolt-slash fa-bug faa-burst faa-slow faa-fast text-warning text-danger text-success')
              .addClass('fa-bolt-slash faa-burst animated faa-slow text-danger');
          });
          socket.addEventListener('error', function(e) {
            ERPro('span > i.websocket', window.top.document)
              .removeClass(ERPro.lo.values(events).join(' '))
              .removeClass('fa-chevrons-down faa-bounce fa-sun-bright fa-bolt-slash fa-bug faa-burst faa-slow faa-fast text-warning text-danger text-success')
              .addClass('fa-bug faa-burst animated faa-slow text-warning');
          });
          socket.addEventListener('message', function(e) {
            if (e.data) {
              if (socket._options.msgpack && e.data instanceof Blob) {
                e.data.arrayBuffer().then(function(buffer) {
                  var data = msgpack.decode(new Uint8Array(buffer));
                  if (data.action) {
                    message(data.action);
                  } else {
                    message('CREATED');
                  }
                });
              } else {
                var data = JSON.parse(e.data);
                if (data.action) {
                  message(data.action);
                } else {
                  message('CREATED');
                }
              }
            }
          });
        }
        return {
          on: function(type, listener) {
            socket.addEventListener(type, function(e) {
              if (e.data) {
                if (socket._options.msgpack && e.data instanceof Blob) {
                  e.data.arrayBuffer().then(function(buffer) {
                    var data = msgpack.decode(new Uint8Array(buffer));
                    if (socket._options.debug) {
                      console.log('RWS> ', data);
                    }
                    listener(data);
                  });
                } else {
                  var data = JSON.parse(e.data);
                  if (socket._options.debug) {
                    console.log('RWS> ', data);
                  }
                  listener(data);
                }
              } else {
                if (socket._options.debug) {
                  console.log('RWS> ', e);
                }
                listener(e);
              }
            });
          },
          send: function(data) {
            if (socket._options.msgpack) {
              if (socket._options.debug) {
                console.log('RWS> ', data);
              }
              socket.send(msgpack.encode(data));
            } else {
              if (socket._options.debug) {
                console.log('RWS> ', data);
              }
              socket.send(JSON.stringify(data));
            }
          },
          ws: socket,
        };
      },
      startup: function() {
      },
      animateCSS: function(element, animation, prefix = 'animate__') {
        return new Promise((resolve, reject) => {
          const animationName = `${prefix}${animation}`;
          const node = typeof element == 'string' ? ERPro(element) : element;
          node.addClass(`${prefix}animated`);
          node.addClass(animationName);

          function handleAnimationEnd(event) {
            node.removeClass(`${prefix}animated`);
            node.removeClass(animationName);
            resolve('Animation ended');
          }

          node.on('animationend', handleAnimationEnd);
        });
      },
      noActivity: function(callback, timeout = 60000 * 10) {
        var idle = false, timer = void (0);
        ERPro('*').bind('mousemove click mouseup mousedown keydown keypress keyup submit change mouseenter scroll resize dblclick', function() {
          clearTimeout(timer);
          if (idle) {
            callback();
          }
          idle = false;
          timer = setTimeout(function() {
            idle = true;
          }, timeout);
        });
        ERPro('body').trigger('mousemove');
      },
    },
  });
})(jQuery);
