import json


def loads(string):
    return json.loads(string)


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False)
