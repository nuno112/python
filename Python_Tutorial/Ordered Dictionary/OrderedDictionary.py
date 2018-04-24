class OrderedDictionary:
    def __init__(self, base={}, **kwargs):
        self._keys = []
        self._values = []
        if type(base) not in (dict, OrderedDictionary):
            raise TypeError("The type used is not a dict")
        for key in base:
            self[key] = base[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def __repr__(self):
        if not self._keys:
            return "{}"
        s = "{"
        for key, value in self.items():
            s += "{0}: {1}, ".format(key, value)
        s = s[0:(len(s)-2)]
        s += "}"
        return s

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._keys

    def __setitem__(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._values.append(value)
            self._keys.append(key)

    def __getitem__(self, key):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        else:
            raise KeyError("The key is not in the dict")

    def __delitem__(self, key):
        if key in self._keys:
            del self._values[self._keys.index(key)]
            del self._keys[self._keys.index(key)]
        else:
            raise KeyError("The key is not in the dict")

    def __iter__(self):
        return iter(self._keys)

    def __add__(self, obj):
        if type(obj) is not type(self):
            raise TypeError("Impossible to add that object")
        else:
            new_dict = OrderedDictionary()
            for key, value in self.items():
                new_dict[key] = value
            for key, value in obj.items():
                new_dict[key] = value
            return new_dict

    def items(self):
        for i, key in enumerate(self._keys):
            yield (key, self._values[i])

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def reverse(self):
        keys = []
        values = []
        for key, value in self.items():
            keys.insert(0, key)
            values.insert(0, value)
        self._keys = keys
        self._values = values

    def sort(self):
        values = list(self._values)
        keys = sorted(self._keys)
        for key, value in self.items():
            values[keys.index(key)] = self._values[self._keys.index(key)]
        self._keys = keys
        self._values = values
