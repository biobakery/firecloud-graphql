
import json
import ast
import collections

def get_class_member_value(obj, levels, subset=False):
    final_value = obj
    for item in levels:
        final_value = getattr(final_value, item)
        if isinstance(final_value, list):
            sub_levels = levels[levels.index(item)+1:]
            if not isinstance(sub_levels, list):
                sub_levels = [sub_levels]
            final_value = [get_class_member_value(sub_value,sub_levels,subset=True) for sub_value in final_value]
            break
    
    if not isinstance(final_value, list) and not subset:
        final_value = [final_value]

    return final_value

def check_for_match(value_selected, hit_values):
    # check if the values for the hit match one or more of the values selected

    match = False
    if isinstance(value_selected, list):
        for item in value_selected:
            if item in hit_values:
                match = True
                break
    elif value_selected in hit_values:
        match = True

    return match

def filter_hits(hits, filters, object_name):
    # Filter the hits based on the json string provided

    if not filters:
        return hits
    
    all_filtered_sets = []
    for content in filters["content"]:   
        field=content["content"]["field"]
        value_selected=content["content"]["value"]

        # check if this filter is for this object
        levels = field.split(".")
        top_level = levels.pop(0)
        if top_level != object_name:
            all_filtered_sets.append(set(hits))
        else:
            filtered_set=set()
            for item in hits:
                hit_values=get_class_member_value(item,levels)
                if check_for_match(value_selected, hit_values):
                    filtered_set.add(item)
            all_filtered_sets.append(list(filtered_set))

    # reduce sets
    final_set = set(all_filtered_sets.pop(0))
    for next_set in all_filtered_sets:
        final_set = final_set.intersection(next_set)

    return list(final_set)

def sort_hits(hits, sort):
    # Sort the hits based on the string provided

    if not sort:
        return hits
   
    sorted_hits = hits
    for content in sort:
        eval_content = ast.literal_eval(content)   
        field=eval_content["field"]
        levels=field.split(".")

        # reverse sort order if set
        order=eval_content["order"]
        reverse_sort_order = False
        if order != "asc":
            reverse_sort_order = True

        # get the values for all of the hits
        hit_value_pairs = []
        for item in sorted_hits:
            hit_value_pairs.append((item, get_class_member_value(item,levels)[0]))

        hit_values = collections.OrderedDict(hit_value_pairs)

        sorted_hits=sorted(hit_values, key=hit_values.get, reverse=reverse_sort_order)

    return sorted_hits

# The functions below were based on code from
# https://github.com/nderkach/python-grahql-api

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

