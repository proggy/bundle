#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module is DEPRECATED, use bundle instead!

This module offers a class called struct, which is basically a dictionary
whose keys may only be strings. In contradiction to normal dictionaries it
offers the possibility to access the values like attributes of classes. So for
example, instead of test['key1'] = value1, you can write test.key1 = value1.
Because its similarity of the builtin type "dict", it has been decided to
deviate from common Python programming standards and to use only lowercase
letters for the name of the class.

Written by Daniel Jung, Jacobs University Bremen, Germany (2011)."""
# 2011-09-13 - 2012-01-03

### call the class "Bundle" in the future! And the module?
### other ideas were Pile, Bunch, Box, Pack, Packet
### the idea "Bunch" originates in matplotlib.cbook.Bunch
### to avoid confusion because of similarity to a C-struct (or even problems
### when working with Cython)


class struct(object):
    """This class is DEPRECATED, use bundle.Bundle instead.

    Basic class that offers structure-/record-like behavior.  Possesses all
    properties of a normal dictionary, but in addition the values may be
    accessed like class attributes (like in "obj.attr"). Furthermore, the keys
    are always sorted alphabetically when accessing the contents, and there is
    a method called "intersection", similar to the builtin type "set"."""
    # 2011-09-13 - 2012-01-03
    # former tb.struct from 2011-01-24 - 2011-06-16

    def __init__(self, *args, **kwargs):
        for arg in args:
            if type(arg).__name__ == 'dict' or type(arg).__name__ == 'struct':
                self.update(arg)
            else:
                raise TypeError

        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __str__(self):
        return ', '.join([str(s)+'='+str(self.__dict__[s])
                          for s in self.keys()])

    def __iter__(self):
        keys = self.keys()
        for key in keys:
            yield key

    def __repr__(self):
        return self.__class__.__name__ + '(' + \
            ', '.join([str(s)+'='+repr(self.__dict__[s])
                       for s in self.keys()]) + ')'

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        delattr(self, key)

    def keys(self):
        keys = self.__dict__.keys()
        keys.sort()
        return keys

    def values(self):
        keys = self.__dict__.keys()
        keys.sort()
        return list([self[key] for key in keys])  # self.__dict__.values()

    def has_key(self, key):
        return key in self.__dict__

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def clear(self):
        return self.__dict__.clear()

    def setdefault(self, key, default):
        return self.__dict__.setdefault(key, default)

    def iterkeys(self):
        return self.__dict__.iterkeys()

    def itervalues(self):
        return self.__dict__.itervalues()

    def iteritems(self):
        return self.__dict__.iteritems()

    def pop(self, key, default=None):
        return self.__dict__.pop(key, default)

    def popitem(self):
        return self.__dict__.popitem()

    def copy(self):
        return struct(self.__dict__)

    def update(self, *args, **kwargs):
        for arg in args:
            if type(arg).__name__ == 'struct':
                self.__dict__.update(arg.__dict__)
            elif type(arg).__name__ == 'dict':
                self.__dict__.update(arg)
            else:
                raise TypeError
        self.__dict__.update(kwargs)

    def __iadd__(self, other):
        self.update(other)
        return self

    def __contains__(self, key):
        return key in self.__dict__

    def __eq__(self, other):
        if not type(other).__name__ == 'struct' \
                and not type(other).__name__ == 'dict':
            raise NotImplementedError('comparison only possible with other ' +
                                      'being of type struct or dict')
        if type(other).__name__ == 'struct':
            return self.__dict__ == other.__dict__
        else:
            return self.__dict__ == other

    def __ne__(self, other):
        return not self == other

    def intersection(self, *others):
        """Return a new structure that contains only elements that are common
        to all of the input structures (with values all being equal)."""
        # 2011-02-07

        # check type of input arguments
        for index, o in enumerate(others):
            if not type(o).__name__ in ['struct', 'dict']:
                raise TypeError('input argument no. %i is neither of type ' +
                                'struct, nor of type dict' % (index+1))

        # initialize output structure
        output = self.copy()

        # go through the other structures and kick out all elements that are
        # not present in this structure, or that do not contain the same values
        for other in others:
            for okey in output.copy():
                if not okey in other:
                    del(output[okey])
                else:
                    if not _equal(output[okey], other[okey]):
                        del(output[okey])

        # return new structure
        return output

    def __and__(self, other):
        """Implement ampersand operator (&). Return new struct that only
        contains elements that are common to both of the input structures (with
        values all being equal)."""
        # 2011-02-07
        return self.intersection(other)


def _equal(*objects):
    """My version of the function "all" with equality check (==), that works
    with all types of objects, even with scalars and nested lists."""
    # 2011-09-13
    # former tb.equal from 2011-02-09
    # former mytools.equal
    if len(objects) > 2:
        a = objects[0]
        for b in objects[1:]:
            if not _equal(a, b):
                return False
        return True
    assert len(objects) == 2, 'at least two objects have to be specified'
    a, b = objects

    if not _isiterable(a) and not _isiterable(b):
        return a == b
    elif _isiterable(a) and _isiterable(b):
        if not _isobject(a) and not _isobject(b):
            if not len(a) == len(b):
                return False
            else:
                for i in xrange(len(a)):
                    if not _equal(a[i], b[i]):
                        return False
                return True
        elif _isobject(a) and _isobject(b):
            return a.__dict__ == b.__dict__
        else:
            return False
    else:
        return False


def _isiterable(obj):
    """Check if an object is iterable. Return True for lists, tuples,
    dictionaries and numpy arrays (all objects that possess an __iter__
    method).  Return False for scalars (float, int, etc.), strings, bool and
    None."""
    # 2011-09-13
    # former tb.isiterable from 2011-01-27
    # former mytools.isiterable
    # inicial idea from
    # http://bytes.com/topic/python/answers/514838-how-test-if-object-sequence-
    # iterable:
    # return isinstance(obj, basestring) or getattr(obj, '__iter__', False)
    # I found this to be better:
    return not getattr(obj, '__iter__', False) is False


def _isobject(obj):
    """Return True if obj possesses an attribute called "__dict__", otherwise
    return False."""
    # 2011-09-13
    # former tb.isobject from 2011-02-09
    # former mytools.isobject
    return not getattr(obj, '__dict__', False) is False
