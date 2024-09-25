
import sys
import os
import json
import ast
import collections

def order_metadata_keys(keys, order):
    new_keys=[]
    for name in order:
        if name in keys:
            new_keys.append(name)
            keys.remove(name)
    new_keys+=keys

    return new_keys

def read_whitelist(filename):
    with open(filename) as infile:
        return set([item.rstrip() for item in infile.readlines()])

def bytes_to_gb(bytes):
    try:
        return int( float(bytes) / (1024**3.0) )
    except ValueError:
        return bytes

class Range(object):
    @staticmethod
    def create_custom(value, offset):
        # require offset to be an int
        offset = int(offset)
        # create a custom range based on the offset provided
        try:
            value = int(float(value))
        except ValueError:
            return value

        search = True
        start = int(value/offset)*offset
        end = start + offset - 1
        while search:
            # check if value is in range
            if value >= start and value <= end:
                search = False
                break
            end += offset
            start += offset

        range ="{0} - {1}".format(start, end)
        return range

    @staticmethod
    def create(value,offset=1,custom=None):
        # generate a range string from the value provided
        # offset of 1 = 10s, 2 = 100s, 3 = 1000s
        start="0"*offset
        end="9"*offset

        # allow for numbers less then 10 that do not
        # require a range
        if offset > 1:
            offset =- 1

        if offset == 0:
            return value

        try:
            bin = str(int(float(value)))[:-1*offset]
            range = "{0}{1} - {0}{2}".format(bin, start, end)
        except ValueError:
            range = value
        return range

    @staticmethod
    def isinstance(value):
        # check if this is a range
        delimiter = " - "
        if not delimiter in value:
            return False

        match = True
        try:
            items = value.split(delimiter)
            start = int(items[0])
            end = int(items[1])
        except ValueError:
            match = False

        return match

    @staticmethod
    def match(range, value_list, field):
        # apply any unit converion included in field
        if field.endswith("file_size"):
            value_list = map(bytes_to_gb, value_list)
        # check if this value is in the range
        start, end = range.split(" - ")
        matches = []
        for value in str_to_float(value_list):
            if value >= int(start) and value <= int(end):
                matches.append(True)
            else:
                matches.append(False)
        return any(matches)

def str_to_float(values, error_zero=False):
    new_values = []
    for v in values:
        try:
            float_value = float(v)
        except ValueError:
            float_value = ""
            if error_zero:
                float_value = 0
        new_values.append(float_value)
    return new_values

def update_max_min(current_values, new_value):
    # ignore non-numeric values
    try:
        new_value = int(float(new_value))
    except ValueError:
        return None
    # update min/max values in dictionary
    if new_value > current_values.get("max",0):
        current_values["max"] = new_value
    if not "min" in current_values:
        current_values["min"] = new_value
    elif new_value < current_values["min"]:
        current_values["min"] = new_value

def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

def get_database_variables():
    try:
        username = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        database = os.environ['MYSQL_DATABASE']
    except KeyError as e:
        print("Unable to find database settings in env variables")
        sys.exit(e)

    return username, password, database

def get_class_member_value(obj, levels, subset=False):
    final_value = obj
    for item in levels:
        try:
            final_value = getattr(final_value, item)
        except AttributeError:
            final_value = 0

        # look for hits subset for possible lists
        if "hits" in dir(final_value):
            final_value = final_value.hits
        if isinstance(final_value, list):
            sub_levels = levels[levels.index(item)+1:]
            if not isinstance(sub_levels, list):
                sub_levels = [sub_levels]
            final_value = [get_class_member_value(sub_value,sub_levels,subset=True) for sub_value in final_value]
            break
    
    if not isinstance(final_value, list) and not subset:
        final_value = [final_value]

    return final_value

def check_for_match(value_selected, hit_values, operation, field):
    # check if the values for the hit match one or more of the values selected

    def is_match(a, b, operation):
        # apply unit conversion, if needed
        if field.endswith("file_size"):
            b = map(bytes_to_gb, b)

        if operation == "in":
            # check for range
            if Range.isinstance(a):
                return Range.match(a,b,field)
            else:
                return True if a in b else False
        elif operation == ">=":
            return any(map(lambda x: x>=float(a), filter(lambda y: y!='None', str_to_float(b))))
        elif operation == "<=":
            return any(map(lambda x: x<=float(a), filter(lambda y: y!='None', str_to_float(b))))
        else:
            print("WARNING: Unexpected operation in filter " + operation)
            return True

    match = False
    if isinstance(value_selected, list):
        for item in value_selected:
            if is_match(item, hit_values, operation):
                match = True
                break
    elif is_match(value_selected, hit_values, operation):
        match = True

    return match

def get_filtered_set(hits, levels, value_selected, operation, field, top_level=None, two_top_levels=None):
    # Search through hits to get filtered set
    filtered_set=set()
    for item in hits:
        if top_level:
            # find object that contains the search values
            hit_values = []
            new_search_subset = []
            for search_item in getattr(item, top_level).hits:
                subset_hit_values = get_class_member_value(search_item, levels)
                if check_for_match(value_selected, subset_hit_values, operation, field):
                    new_search_subset.append(search_item)
                hit_values+=subset_hit_values
            # remove filtered objects
            #getattr(item, top_level).hits = new_search_subset
        elif two_top_levels:
            hit_values = []
            for search_item in getattr(item, two_top_levels[0]).hits:
                for search_item_two in getattr(search_item, two_top_levels[1]):
                    hit_values+=get_class_member_value(search_item_two, levels)
        else:
            hit_values=get_class_member_value(item,levels)

        if check_for_match(value_selected, hit_values, operation, field):
            filtered_set.add(item)
    return list(filtered_set)

def subhits(single_hit, top_level):
    # search for item with subhits
    levels = []
    for item in dir(single_hit):
        sub_hit = getattr(single_hit, item)
        if "hits" in dir(sub_hit):
            try:
                for subitem in dir(sub_hit.hits[0]):
                    if isinstance(getattr(sub_hit.hits[0], subitem), list):
                        if subitem == top_level:
                            levels = [item, subitem]
            except IndexError:
                continue
    return levels

def filter_hits(hits, filters, object_name, project_access):
    # Filter the hits based on the json string provided

    MIN_RESTRICTED_HITS=20

    if not filters:
        return hits

    if not "content" in filters:
        return hits

    if not hits:
        return hits

    all_filtered_sets = []
    for content in filters["content"]:   
        field=content["content"]["field"]
        value_selected=content["content"]["value"]
        operation=content["op"]

        # check if this filter is for this object
        levels = field.split(".")
        top_level = levels.pop(0)
        if top_level != object_name:
            if levels[0] == object_name:
                try:
                    top_level = levels.pop(0)
                    all_filtered_sets.append(get_filtered_set(hits, levels, value_selected, operation, field))
                except IndexError:
                    continue
            elif levels[0] in dir(hits[0]):
                all_filtered_sets.append(get_filtered_set(hits, levels, value_selected, operation, field))
            elif top_level in dir(hits[0]):
                all_filtered_sets.append(get_filtered_set(hits, levels, value_selected, operation, field, top_level))
            else:
                sub_hit_levels = subhits(hits[0],top_level)
                if sub_hit_levels:
                    all_filtered_sets.append(get_filtered_set(hits, levels, value_selected, operation, field, two_top_levels=sub_hit_levels))
                else:
                    all_filtered_sets.append(set(hits))
        else:
            all_filtered_sets.append(get_filtered_set(hits, levels, value_selected, operation, field))

    # reduce sets
    try:
        final_set = set(all_filtered_sets.pop(0))
    except IndexError:
        final_set = []

    for next_set in all_filtered_sets:
        final_set = final_set.intersection(next_set)

    final_set=list(final_set)

    # if this is not an authenticated user then check to make sure there are enough hits
    # allow for filtering of files using just file based filters
    if len(filters["content"]) == 1 and filters["content"][0].get("content",{}).get("field","").startswith("files."):
        return final_set
    # allow for filtering of program through participant tab
    elif len(filters["content"]) == 1 and filters["content"][0].get("content",{}).get("field","") == "cases.project.program.name":
        return final_set
    # allow for combinations of project and files filters (all no auth)
    elif len(filters["content"]) == get_total_noauth_content_filters(filters):
        return final_set
    elif not project_access and len(final_set) < MIN_RESTRICTED_HITS:
        # return empty set for security filter
        return []
    else:
        return final_set

def get_total_noauth_content_filters(filters):
    # return the total number of no auth required filters
    # currently just program name from cases plus all files filters are no auth

    return len(filter(lambda x: x.get("content",{}).get("field","") == "cases.project.program.name" or x.get("content",{}).get("field","").startswith("files."),filters["content"]))

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

def offset_hits(hits, offset):
    if not offset:
        offset = 0
    class TotalList(list):
        def __init__(self, newlist, total):
            super(TotalList, self).__init__(newlist)
            self.total = total
    return TotalList(hits[offset:], len(hits[offset:]))

# The functions below were based on code from
# https://github.com/nderkach/python-grahql-api

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

