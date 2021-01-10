# coding=utf8
import json
from datetime import datetime, date


class SmartEncoder(json.JSONEncoder):
    '''
        只支持一层解析。
    '''
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def json_encode(obj):
    '''
    >>> from datetime import datetime
    >>> json_encode(dict((
        ('a', 'b'),
        ('c', datetime.now()),
        )))
    >>> ''
    '''
    return json.dumps(obj, cls=SmartEncoder)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    obj = [dict((
        ('a', 'b'),
        ('c', datetime.now()),
        )), ]
    print(json_encode(obj))
    obj2 = {
        'a': obj,
        'b': ''
        }
    print(json_encode(obj2))
