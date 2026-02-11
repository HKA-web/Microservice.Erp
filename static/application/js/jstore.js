(function () {
  'use strict';

  function jStore() {
    function Store(name, serializer) {
      if (!this.localStorage) {
        throw 'localStorage: Environment does not support localStorage.'
      }
      this.name = name;
      this.serializer = serializer || {
        serialize: function (item) {
          return isObject(item) ? JSON.stringify(item) : item;
        },
        deserialize: function (data) {
          return data && JSON.parse(data);
        }
      };
      var store = this.localStorage().getItem(this.name);
      this.records = (store && store.split(',')) || [];
    }

    Store.prototype = {
      save: function () {
        this.localStorage().setItem(this.name, this.records.join(','));
      },
      create: function (model) {
        if (!model.id && model.id !== 0) {
          model.id = guid();
          model.set(model.idAttribute, model.id);
        }
        this.localStorage().setItem(this._itemName(model.id), this.serializer.serialize(model));
        this.records.push(model.id.toString());
        this.save();
        return this.find(model);
      },
      update: function (model) {
        this.localStorage().setItem(this._itemName(model.id), this.serializer.serialize(model));
        var modelId = model.id.toString();
        if (!contains(this.records, modelId)) {
          this.records.push(modelId);
          this.save();
        }
        return this.find(model);
      },
      find: function (model) {
        return this.serializer.deserialize(this.localStorage().getItem(this._itemName(model.id)));
      },
      findAll: function () {
        var result = [];
        for (var i = 0, id, data; i < this.records.length; i++) {
          id = this.records[i];
          data = this.serializer.deserialize(this.localStorage().getItem(this._itemName(id)));
          if (data != null) result.push(data);
        }
        return result;
      },
      destroy: function (model) {
        this.localStorage().removeItem(this._itemName(model.id));
        var modelId = model.id.toString();
        for (var i = 0, id; i < this.records.length; i++) {
          if (this.records[i] === modelId) {
            this.records.splice(i, 1);
          }
        }
        this.save();
        return model;
      },
      nextId: function () {
        return this.records.length === 0 ? 1 : Number(this.records[this.records.length - 1]) + 1;
      },
      localStorage: function () {
        return localStorage;
      },
      _clear: function () {
        var local = this.localStorage(),
          itemRe = new RegExp('^' + this.name + '-');
        local.removeItem(this.name);
        for (var k in local) {
          if (itemRe.test(k)) {
            local.removeItem(k);
          }
        }
        this.records.length = 0;
      },
      _storageSize: function () {
        return this.localStorage().length;
      },
      _itemName: function (id) {
        return this.name + '-' + id;
      }
    };
    return Store;

    function S4() {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }

    function guid() {
      return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4());
    }

    function isObject(item) {
      return item === Object(item);
    }

    function contains(array, item) {
      var i = array.length;
      while (i--) if (array[i] === item) return true;
      return false;
    }
  }
})();
