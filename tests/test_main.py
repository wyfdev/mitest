from pytest import raises
from mitest import (
    TestPolicy,
    PolicySyntaxErrorException,
    DataKeyErrorException
)


def test_and():
    policys = {
        'mongo_style': {
            '$and': [
                {'a': '23'},
                {'$and': [
                    {'b': {'$gte': 2}},
                    {'b': {'$lt': 4}}
                ]}
            ]
        },
        'simplify_remove_and': [
            {'a': '23'},
            [
                {'b': {'$gte': 2}},
                {'b': {'$lt': 4}}
            ]
        ],
        'simplify_merge_list_itmes_of_same_key': [
            {'a': '23'},
            [
                {'b': [{'$gte': 2}, {'$lt': 4}]}
            ]
        ],
        'simplify_merge_remove_list': {'a': '23', 'b': {'$gte': 2, '$lt': 4}}
    }

    for policy in policys.values():
        policy = TestPolicy(policy)

        result = policy.test({'a': '23', 'b': 3})
        assert result

        result = policy.test({'a': '23', 'b': 2})
        assert result
        assert len(result.how) == 3
        assert ('a', {'$eq': '23'}, '23') in result.how
        assert ('b', {'$gte': 2}, 2) in result.how
        assert ('b', {'$lt': 4}, 2) in result.how

        result = policy.test({'a': '23', 'b': 1})
        assert bool(result) is False
        assert result.how == [('b', {'$gte': 2}, 1)]


def test_or():
    policys = {
        'mongo_style': {
            '$or': [
                {'a': '23'},
                {'$and': [
                    {'b': {'$gte': 2}},
                    {'b': {'$lt': 5}},
                    {'b': {'$neq': 3}}
                ]}
            ]
        },
        'simplie': {
            '$or': [
                {'a': '23'},
                {'b': {'$gt': 2, '$lte': 5, '$neq': 3}}
            ]
        }
    }
    for policy in policys.values():
        policy = TestPolicy(policy)

        result = policy.test({'a': '23', 'b': 4})
        assert result
        # assert bool(result) is


def test_exceptions():
    # policy: key under other key
    policy = TestPolicy({'a': {'b': 10}})
    with raises(PolicySyntaxErrorException) as err:
        policy.test({'a': '23', 'b': 4})
        assert err.value.args[0] == \
            'Variable under sub policy of other variable'

    # data: has not key in policy
    policy = TestPolicy({'a': {'$lt': 10}})
    with raises(DataKeyErrorException) as err:
        policy.test({})


def test_special_case():
    # empty string key is also lagal key
    policy = TestPolicy({'': {'$eq': 'empty_string_key'}})
    result = policy.test({'': 'empty_string_key'})
    assert bool(result) is True

    # type struct
    policy = TestPolicy({'a': 10})      # int
    result = policy.test({'a': '10'})   # string
    assert bool(result) is False

    # type error
    policy = TestPolicy({'a': {'$lt': 10}})
    with raises(TypeError):
        policy.test({'a': '10'})
