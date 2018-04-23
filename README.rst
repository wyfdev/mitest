mitest - Mongo Inspired policy test
===================================

.. image:: https://travis-ci.org/WYFDEV/mitest.svg?branch=master
    :target: https://travis-ci.org/WYFDEV/mitest

Introduction
------------

Test if data match policy, inspired by
`MongoDB query format <https://docs.mongodb.com/manual/tutorial/query-documents/>`_

A **policy** express the expected *relationship* between *variable* and *data*
uesing json (or python dict direct).

Key beginning with "$" to indicate relationship like `$and`, `$lt`, `$gte`.


Example
-------

policy, variable "a" less then 10::

    {"a": {"$lt": 10}}

test, if given data match policy::

    >>> policy = TestPolicy({'a': {'$lt': 10}})
    >>>
    >>> result = policy.test({'a': 9})
    >>> bool(result)
    True
    >>> result.how
    [('a', {'$lt': 10}, 9)]
    >>>
    >>> result = policy.test({'a': 11})
    >>> bool(result)
    False
    >>> result.how
    [('a', {'$lt': 10}, 11)]

Arrtibute `how` express how data match or not match policy.
For example, `("a", {"$lt": 10}, 9)` mean that for variable `a`, policy is `lessthen 2`,
and (or but, if not match) given data is `9`.


Policy format
-------------

MongoDB query format is a little complicated, but
"Simple is better than complex".

For this MongoDB query::

    {"$or":[
        {"$and":[
            {"a":"23"},
            {"b":6}
        ]},
        {"$and":[
            {"c":{"$gte":2}},
            {"c":{"$lt":4}}
        ]}
    ]}

"$and" is default for each items in list::

    {"$or":[
        [
            {"a":"23"},
            {"b":6}
        ],
        [
            {"c":{"$gte":2}},
            {"c":{"$lt":4}}
        ]
    ]}

Merge items to single dict::

    {"$or":[
        {"a":"23", "b":6},
        {"c":{"$gte":2, "$lt":4}}
    ]}

Much simpler :-)


Wish this can help you.
