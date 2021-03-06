#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2013-2017 Daniel Jung
# Contact: djungbremen@gmail.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""Implement a dictionary-like class *Bundle*, which enables attribute-like
access to its elements. So, for example, instead of

>>> bundle['key1'] = 'hello'

you can also do

>>> bundle.key1 = 'hello'

The same is true for reading access:

>>> bundle.key1
hello

Another extension is the method *intersection()*, which is the equivalent to
the method of the *set* type with the same name.


Limitations
-----------

In contrast to conventional dictionaries, keys must be strings."""
# 2012-06-05
# 2017-04-12
# based on structure.py (2011-09-13 - 2012-01-03)
import collections


class Bundle(collections.MutableMapping):
    """Dictionary-like data structure (actually wraps a dictionary, and
    provides a dictionary-like interface), but with the following changes:

    1. Elements can also be accessed like attributes, e.g. `a.b = c` instead of
       `a['b'] = c`.
    2. Because of the above, all keys have to be strings.
    3. Added set-like methods, like "intersection"."""
    __created__ = '2012-06-05'
    __modified__ = '2013-08-01'
    # former structure.struct from 2011-09-13 until 2012-01-03 (completely
    # rewritten)
    # former tb.struct from 2011-01-24 until 2011-06-16

    def __init__(self, arg=None, **kwargs):
        """Bundle() -> new empty bundle
        Bundle(mapping)  -> new bundle initialize from a mapping object's
                            (key, value) pairs
        Bundle(iterable) -> new bundle initialized as if via:
                            b = Bundle()
                            for key, value in iterable:
                            b[key] = value
        Bundle(**kwargs) -> new bundle initialized with the name=value pairs in
                            the keyword argument list. For example:
                            Bundle(one=1, two=2)"""
        # 2012-06-11 - 2012-06-11
        # initialize data structure
        self.__data = {} if arg is None else dict(arg)

        # check for non-string keys
        for key in self.__data:
            if not isinstance(key, basestring):
                raise TypeError('the key "%s" is not a string' % key)

        # add keyword arguments
        self.update(kwargs)

    def __iter__(self):
        # 2012-12-15
        keys = self.__data.keys()
        keys.sort()
        return iter(keys)

    def __getitem__(self, key):
        return self.__data[key]

    def __len__(self):
        return len(self.__data)

    def __setitem__(self, key, value):
        if not isinstance(key, basestring):
            raise TypeError('the key "%s" is not a string' % key)
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __setattr__(self, name, value):
        if name == '_%s__data' % self.__class__.__name__:
            self.__dict__[name] = value
        else:
            self[name] = value

    def __getattr__(self, name):
        try:
            if name == '_%s__data' % self.__class__.__name__:
                return self.__dict__[name]
            else:
                return self.__data[name]
        except KeyError, e:
            # important when trying to pickle a bundle
            raise AttributeError(e)

    def __delattr__(self, name):
        if name == '_%s__data' % self.__class__.__name__:
            raise KeyError('impossible to delete attribute %s' % name)
        del self[name]

    def __repr__(self):
        # 2012-12-15 - 2012-12-15
        #keys = self.__data.keys()
        #keys.sort()
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(('%s=%s' % (key, repr(value))
                                     for key, value in self.iteritems())))

    def __and__(self, other):
        """Implement ampersand operator (&). Return new struct that only
        contains elements that are common to both of the input structures (with
        values all being equal)."""
        # 2011-02-07
        return self.interaction(other)

    def intersection(self, *others):
        """Return intersection of the given bundles, containing only key-value
        pairs that are equal in all the bundles."""
        # 2012-06-05 - 2013-10-31
        # former structure.struct.intersection from 2011-02-07

        # check types
        #for index, other in enumerate(others):
        #  #if not type(other) in [Bundle, dict]:
        #  if not isinstance(other, (Bundle, dict)):
        #    raise TypeError, 'input argument no. %i ' % (index+1)+\
        #                     'is neither of type Bundle, nor of type dict'

        # create output bundle
        output = self.copy()

        # cycle other bundles and kick out all elements that are not
        # present in this structure, or that do not contain the same values
        for other in others:
            for okey in output.keys():
                if not okey in other:
                    del(output[okey])
                else:
                    try:
                        if output[okey] != other[okey]:
                            del(output[okey])
                    except ValueError:
                        del(output[okey])

        # return new bundle
        return output

    def copy(self):
        return self.__class__(self)
    
    def __dir__(self):
        return self.__data.keys()
    
    def _ipython_key_completions_(self):
        return self.__data.keys()


#================================================================#
# functions that operate on Bundle objects                       #
#================================================================#


def intersection(*bundles):
    """Return intersection of the given bundles, containing only key-value
    pairs that are equal in all of the bundles.

    To be clear: Both key AND value have to agree among all of the input
    bundles, otherwise a key-value pair does not appear in the output
    bundle."""
    # 2012-11-13 - 2012-11-13
    return Bundle(bundles[0]).intersection(*bundles[1:])


def __main__():
    import doctest
    doctest.testmod()
