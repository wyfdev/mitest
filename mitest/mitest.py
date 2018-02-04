'''
MongoDB Inspired policy test

>>> policy = {'a':{'$gt': 1}, '$or':[{'b':{'$lt': 100, '$gt': 0}}, {'c': 'foo'}]}
>>> data = {'a': 2, 'b': 50, 'c': 'bar'}
>>> result = TestPolicy(policy).test(data)
>>> bool(result)
True
>>> result.how
[('a', {'$gt': 1}, 2), ('b', {'$lt': 100}, 50), ('b', {'$gt': 0}, 50)]

'''

from typing import Any, NewType, Union, List
from copy import deepcopy


PolicyDict = NewType('PolicyDict', dict)    # policy
TargetDict = NewType('TargetDict', dict)    # target data of test


class TestPolicy(object):

    def __init__(self, policy: PolicyDict):
        '''
        :param policy: policy expression
        '''
        self.policy = policy

    def test(self, target: TargetDict) -> 'Test':
        '''test if target match policy
        :param target: target to test, in dict
        :return: Test object
        '''
        return Test(deepcopy(self.policy), target)


class Test(object):

    def __init__(self, policy: TestPolicy, target: TargetDict):
        '''
        :param plicy: policy object
        :param target: test target, in dict
        '''
        self.target = target
        # current
        self.key = None
        self.value = None
        # how
        self.match = list()
        self.not_match = list()
        # start test
        self.result = self.test('$and', policy)

    def __bool__(self):
        return self.result

    @property
    def how(self) -> list:
        '''
        :return: how target match policy or not match policy
            format like [(key, (policy, value_of_policy"), value_of_actual_value), ...]
        '''
        return self.match if self else self.not_match

    def test(self, k: str, v: Any) -> bool:
        '''test if data match policy, recursive, recoreding match and not match'''
        match = None
        try:
            if k[0] == '$':
                # {'$relationship': <sub_policy or value_judgement>}
                if k not in ('$and', '$or'):
                    match = (self.key, {k: v}, self.value)
                assert getattr(self, k.replace('$', '_'))(v)
            elif not isinstance(v, (dict, list)):
                # {'var': <value>}  equal  {'var': {'$eq': <value>}}
                match = (k, {'$eq': v}, v)
                assert self.target[k] == v
            else:
                # {'var', <sub_policy in dict or list>}
                self.key = k
                self.value = self.target[k]
                return all([self.test(subk, subv) for subk, subv in self._ensure_items(v)])
        except AssertionError:
            if match is not None: self.not_match.append(match)
            return False
        except Exception:
            raise
        else:
            if match is not None: self.match.append(match)
            return True

    @classmethod
    def _ensure_items(cls, data: Union[list, dict]):
        items = []
        def traverse(t):
            if isinstance(t, dict):
                items.extend(t.items())
            elif isinstance(t, list):
                for i in t: traverse(i)
            else:
                raise Exception('Unexcepted value', t)
        traverse(data)
        return items

    def _and(self, t):
        return all([self.test(k, v) for k, v in self._ensure_items(t)])

    def _or(self, t):
        return any([self.test(k, v) for k, v in self._ensure_items(t)])

    def _eq(self, v):
        return self.value == v

    def _neq(self, v):
        return self.value != v

    def _lt(self, v):
        return self.value < v

    def _gt(self, v):
        return self.value > v

    def _lte(self, v):
        return self.value <= v

    def _gte(self, v):
        return self.value >= v

