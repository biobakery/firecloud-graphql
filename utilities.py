
import json
import collections

# The functions were based on code from
# https://github.com/nderkach/python-grahql-api

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

