import collections


class AnyMethod(object):
    """ Instances of that class can call any nonexistent
        own method. If called method exists it will be called,
        if method is not exists, will be called default method,
        that does nothing.

        This class was created to use functions, that uses
        passed logger (instance of logging) received in arguments.
        This class substitute logger in tests, so logger.info(),
        logger.debug() etc. does nothing without some problems
        and without need to import logging.
    """

    def __getattribute__(self, item):
        try:
            res = super(AnyMethod, self).__getattribute__(item)
            return res
        except AttributeError:
            return self.__anymethod

    def __anymethod(self, *args, **kwargs):
        pass


class CaseInsensitiveGroupedDict(collections.MutableMapping):
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        self._groups = dict()
        if data is None:
            data = dict()
        self.update(data, *kwargs)

    def __setitem__(self, key, value):
        group = 'default'
        if isinstance(key, tuple):
            if len(key) == 2:
                group = key[1]
                key = key[0]
            else:
                raise TypeError("tuple must be with 2 values (key, group), "
                                "{} given".format(len(key)))
        lower_key = key.lower()
        group = group.lower()
        if lower_key in self._groups and self._groups[lower_key] != 'default':
            group = self._groups[lower_key]
        self._store[lower_key] = (key, value)
        self._groups[lower_key] = group

    def __getitem__(self, item):
        return self._store[item.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]
        del self._groups[key.lower()]

    def __iter__(self):
        return (cased for cased, value in self._store.values())

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if not isinstance(other, CaseInsensitiveGroupedDict):
            return NotImplemented
        return self.gdictlower() == other.gdictlower()

    def __repr__(self):
        return str(dict(self._store.values()))

    def gdictlower(self):
        """ Returns dict where keys is a tuple (key, group)
            like {(key1, group1): val1, (key2, group2): val2)...}
            keys and groups in lower case
        """
        res = {}
        for key in self._store:
            res[key, self.getgroup(key)] = self[key]
        return res

    def gdict(self):
        """ Returns dict where keys is a tuple (key, group)
            like {(key1, group1): val1, (key2, group2): val2)...}
            keys in original case and groups in lower case
        """
        res = {}
        for key, value in self._store.values():
            res[key, self.getgroup(key)] = value
        return res

    def getgroup(self, key):
        """ Returns a group of a key
        :param key: key in any case
        :return: group of key
        """
        return self._groups[key.lower()]

    def setgroup(self, key, group):
        """ Set new group for a key
        :param key:  key in any case
        :param group: group in any case (will be saved in
               lower case)
        :return: None
        """
        if key.lower() not in self:
            raise KeyError(key)
        self._groups[key.lower()] = group.lower()

    def getgroupdictlower(self, group):
        """
        :param group: group in any case
        :return: dictionary {'key': 'value'} of all keys
                 belong to group
        """
        keys = self.getgroupkeyslower(group)
        res = {}
        for key in keys:
            res[key] = self[key]
        return res

    def getgroupkeyslower(self, group):
        """
        :param group: group in any case
        :return: list of keys in lower case belong to group
        """
        keys = []
        group = group.lower()
        if group in self._groups.values():
            keys = filter(lambda x: self._groups[x]==group, self._groups.keys())
        return keys

    def getgroupkeys(self, group):
        """
        :param group: group in any case
        :return: list of keys in original case belong to group
        """
        keys = self.getgroupkeyslower(group)
        keys = map(lambda x: self._store[x][0], keys)
        return keys

    def getgroupkeysupper(self, group):
        """
        :param group: group in any case
        :return: list of keys in upper case belong to group
        """
        keys = self.getgroupkeyslower(group)
        keys = map(lambda x: x.upper(), keys)
        return keys

    def delgroup(self, group):
        """ Delete all keys belong to group
        :param group: Group to delete
        :return: None
        """
        keys = list()
        if group in self._groups.values():
            keys = filter(lambda x: x[1] == group, self._groups.items())
        for key, group in keys:
            del self[key]

    def regroup(self, group, newgroup='default'):
        """ Rename group
        :param group: Group to rename
        :param newgroup: New name for group
        :return: None
        """
        group = group.lower()
        newgroup = newgroup.lower()
        for key in self._groups:
            self._groups[key] = newgroup if self._groups[key]==group else self._groups[key]

    def lower_items(self):
        return ((l, kv) for (l, kv) in self._store.items())

    def groupsset(self):
        """
        :return: set of groups
        """
        return set(self._groups.values())

    def groups(self):
        """
        :return: list of groups
        """
        return list(self.groupsset())

    def copy(self):
        return CaseInsensitiveGroupedDict(((key, self.getgroup(key)), value) for key, value in self._store.values())

    def extend(self, other):
        if isinstance(other, dict):
            other = CaseInsensitiveGroupedDict(other)
        if not isinstance(other, CaseInsensitiveGroupedDict):
            return
        for key, kval in other.lower_items():
            if key not in self:
                self[kval[0], other.getgroup(key)] = kval[1]

