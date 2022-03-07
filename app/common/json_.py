from datetime import date, datetime
from decimal import Decimal
import json

TYPES_DUMP = {
    'Decimal': str,
    'date': str,
    'datetime': str,
}
TYPES_LOAD = {
    'Decimal': Decimal,
    'date': date.fromisoformat,
    'datetime': datetime.fromisoformat,
}


def recursive_dump(obj, types=TYPES_DUMP):
    r = obj
    if isinstance(obj, dict):
        r = {}
        for k, v in obj.items():
            t = type(v).__name__
            if t in types:
                r[f'{k}:{t}'] = types[t](v)
            elif t == 'list':
                r[k] = recursive_dump(v)
            else:
                r[k] = v
    elif isinstance(obj, list):
        r = []
        for v in obj:
            r += [recursive_dump(v)]
    return r


def recursive_load(obj, types=TYPES_LOAD):
    r = obj
    if isinstance(obj, dict):
        r = {}
        for kt, v in obj.items():
            if isinstance(v, list):
                r[kt] = recursive_load(v)
            else:
                try:
                    k, t = kt.split(':', 1)
                    r[k] = types[t](v)
                except ValueError:
                    r[kt] = v
    elif isinstance(obj, list):
        r = []
        for v in obj:
            r += [recursive_load(v)]
    return r


def dump(obj, **kwargs):
    kwargs['ensure_ascii'] = False
    return json.dumps(recursive_dump(obj), **kwargs)


def load(obj, **kwargs):
    return recursive_load(json.loads(obj, **kwargs))


if __name__ == '__main__':
    test1 = {
        'a': 1,
        'b': 'й',
        'c': 2.3,
        'd': date.today(),
        'e': Decimal('1.2'),
        'f': datetime.today(),
        'h': [{'a': 1, 'b': Decimal('3.4')}],
        'j': [1, 2, 3],
    }
    str_ = dump(test1)
    assert 'b:Decimal' in str_
    assert 'd:date' in str_
    assert 'e:Decimal' in str_
    assert 'f:datetime' in str_
    test2 = load(str_)
    assert test1 == test2
