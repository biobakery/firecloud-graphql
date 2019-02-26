
import json
import collections

def get_class_member_value(obj,members,offset=1):
    levels = members.split(".")[offset:]
    final_value = getattr(obj, levels.pop(0))
    for item in levels:
        final_value = getattr(final_value, item)

        if isinstance(final_value, list):
            sub_levels = ".".join(levels[levels.index(item)+1:])
            final_value = [get_class_member_value(sub_value,sub_levels,offset=0) for sub_value in final_value]
            break
    
    if not isinstance(final_value, list) and offset !=0:
        final_value = [final_value]

    return final_value

def filter_hits(hits, filters):
    # Filter the hits based on the json string provided

    if not filters:
        return hits

    filtered_set = set()
    for content in filters["content"]:   
        field=content["content"]["field"]
        value_selected=content["content"]["value"][0]
        for item in hits:
            hit_values=get_class_member_value(item,field)
            if value_selected in hit_values:
                filtered_set.add(item)
    return list(filtered_set)

# The functions were based on code from
# https://github.com/nderkach/python-grahql-api

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

