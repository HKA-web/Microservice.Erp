(function (jQuery) {
  var topics = {}, uid = -1
  jQuery.extend({
    publish: function (topic, data) {
      if (!topics[topic]) {
        return false;
      }
      setTimeout(function () {
        var subscribers = topics[topic],
          length = subscribers ? subscribers.length : 0;
        while (length--) {
          subscribers[length].callback(topic, data);
        }
      }, 0);
      return true;
    },
    subscribe: function (topic, callback) {
      if (!topics[topic]) {
        topics[topic] = [];
      }
      var token = (++uid).toString();
      topics[topic].push({
        token: token,
        callback: callback
      });
      return token;
    },
    unsubscribe: function ( token ) {
      for (var topic in topics) {
        if (topics[topic]) {
          for (var loop = 0, length = topics[topic].length; loop < length; loop++) {
            if (topics[topic][loop].token === token) {
              topics[topic].splice(loop, 1);
              return token;
            }
          }
        }
      }
      return false;
    },
    topics: function () {
      return topics;
    },
    example: function () {
      var subscription = jQuery.subscribe( 'example1', function(topics, data){
        console.log({[topics]: data});
      } );
      jQuery.publish('example1', 'hello world!');
      jQuery.publish('example1', ['test','a','b','c']);
      jQuery.publish('example1', [{'color':'blue'},{'text':'hello'}]);
      setTimeout(function() {
          jQuery.unsubscribe(subscription);
      }, 0);
      jQuery.publish('example1', 'hello again!');
      console.log(jQuery.topics())
    }
  });
})(jQuery);
