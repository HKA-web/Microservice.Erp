; (function ($) {
    'use strict';

    var dataPrefix = 'data-';

    $.fn.dataSubset = function (prefix, removePrefix) {
        var data,
            tempContainer,
            filter;

        if (typeof removePrefix === 'undefined') {
            removePrefix = true;
        } else {
            if (typeof removePrefix !== 'boolean') {
                throw new Error('RemovePrefix parameter must be a boolean');
            }
        }

        if (typeof prefix === 'undefined') {
            data = this.data();
        } else {
            prefix = prefix.replace(dataPrefix, '');

            if (typeof prefix === 'string' && prefix) {
                if (this.length) {
                    data = {};
                    tempContainer = $('<div></div>');
                    filter = dataPrefix + prefix + '-';

                    $.each(this[0].attributes, function (index, attribute) {
                        var name = attribute.name,
                            value = attribute.value;

                        if (name.indexOf(filter) === 0) {
                            name = removePrefix ? name.substring(filter.length) : name.substring(dataPrefix.length);
                            name = name.replace(/^-+|-+$/g, '');
                            tempContainer.attr(dataPrefix + name, value);
                        }
                    });

                    data = tempContainer.data();
                    tempContainer.remove();
                }
            } else {
                throw new Error('Prefix parameter must be a non-empty string');
            }
        }

        return data;
    };
})(jQuery);