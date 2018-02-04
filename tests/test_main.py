from mitest import TestPolicy


def test_and():
    policys = {
        'mongo_style': {
            "$and": [
                {"a":"23"},
                {"$and":[
                    {"b":{"$gte":2}},
                    {"b":{"$lt":4}}
                ]}
            ]
        },
        'simplify_remove_and': [
            {"a":"23"},
            [
                {"b":{"$gte":2}},
                {"b":{"$lt":4}}
            ]
        ],
        'simplify_merge_list_itmes_of_same_key': [
            {"a":"23"},
            [
                {"b":[{"$gte":2}, {"$lt":4}]}
            ]
        ],
        'simplify_merge_remove_list': {"a":"23", "b":{"$gte":2, "$lt":4}}
    }

    for policy in policys.values():
        policy = TestPolicy(policy)

        result = policy.test({"a": "23", "b": 3})
        assert result

        result = policy.test({"a": "23", "b": 2})
        assert result
        assert len(result.how) == 3
        assert ('a', {'$eq': '23'}, '23') in result.how
        assert ('b', {'$gte': 2}, 2) in result.how
        assert ('b', {'$lt': 4}, 2) in result.how

        result = policy.test({"a": "23", "b": 1})
        assert bool(result) is False
        assert result.how == [('b', {'$gte': 2}, 1)]

def test_or():
    policys = {
        'mongo_style': {
            "$or": [
                {"a":"23"},
                {"$and":[
                    {"b":{"$gte":2}},
                    {"b":{"$lt":4}}
                ]}
            ]
        },
        'simplie': {
            "$or": [
                {"a":"23"},
                {"b":{"$gt":2, "$lte":4}}
            ]
        }
    }
    for policy in policys.values():
        policy = TestPolicy(policy)

        result = policy.test({"a": "23", "b": 4})
        assert result
        # assert bool(result) is
