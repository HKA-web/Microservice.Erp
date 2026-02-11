var lazyload = lazyload || {};
(function($, lazyload) {
	'use strict';
	var loaded = [],
	promise = false,
	deferred = $.Deferred();
	lazyload.load = function (srcs) {
		srcs = $.isArray(srcs) ? srcs : srcs.split(/\s+/);
		if(!promise){
			promise = deferred.promise();
		}
		$.each(srcs, function(index, src) {
			promise = promise.then( function(){
				return loaded[src] ? loaded[src].promise() : (src.indexOf('.css') >=0 ? loadCSS(src) : loadScript(src));
			} );
		});
		deferred.resolve();
		return promise;
	};
	lazyload.unload = function(srcs){
		srcs = $.isArray(srcs) ? srcs : srcs.split(/\s+/);
		$.each(srcs, function(index, src) {
			src.indexOf('.css') >=0 ? $('link[href=\''+src+'\']').remove() : $('script[src=\''+src+'\']').remove();
			delete loaded[src];
		});
	};
	var loadScript = function (src) {
		var deferred = $.Deferred();
		var script = document.createElement('script');
		script.src = src;
		script.onload = function (e) {
			deferred.resolve(e);
		};
		script.onerror = function (e) {
			deferred.reject(e);
		};
		document.body.appendChild(script);
		loaded[src] = deferred;
		return deferred.promise();
	};
	var loadCSS = function (href) {
		var deferred = $.Deferred();
		var style = document.createElement('link');
		style.rel = 'stylesheet';
		style.type = 'text/css';
		style.href = href;
		style.onload = function (e) {
			deferred.resolve(e);
		};
		style.onerror = function (e) {
			deferred.reject(e);
		};
		var head = document.getElementsByTagName('head')[0]
		head.insertBefore(style, head.firstChild);
		loaded[href] = deferred;
		return deferred.promise();
	};
})(jQuery, lazyload);
