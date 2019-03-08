

# Code to query the firecloud api

import json 

from firecloud import api, errors

NAMESPACE="firecloud-biom-mass"

def call_api(url):
    """ Use the firecloud api module to query firecloud 
        Allows for additional options not included in fiss api"""
    result = api.__get(url)
    try:
        api._check_response_code(result, 200)
        result = result.json()
    except errors.FireCloudServerError as e:
        print("Error with api query ")
        print(e)
        result = {}
    return result

def get_entities(namespace, workspace, entity_type):
    url = "workspaces/{0}/{1}/entities/{2}".format(namespace,workspace,entity_type)
    json_result = call_api(url)
    return json_result

def get_workspaces(namespace):
    # This is based on the fiss list_spaces function but only workspaces are returned

    workspaces = api.list_workspaces()
    api._check_response_code(workspaces, 200)

    for space in workspaces.json():
        if namespace == space['workspace']['namespace']:
            yield space['workspace']['name']

def extract_values(obj):
    """Pull all values recursively from nested JSON."""
    arr = []
    def extract(obj, arr):
        """Recursively search for values in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr)
                else:
                    arr.append(str(v))
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr)
        return arr

    results = extract(obj, arr)
    return results

def get_all_workspace_data():
    # search through all of the workspaces in the namespace 
    values_file_samples = list()
    values_participants = list()
    keys_file_samples = list()
    for workspace in get_workspaces(NAMESPACE):
        print("Gather data from " + workspace)
        samples = get_entities(NAMESPACE,workspace,"sample")
                  
        for item in samples:
             values = extract_values(item['attributes'])
             values.insert(0,item['name'])
             values.pop(3)
             values.insert(0,workspace)
             print("File sample values",values)
             values_file_samples.append(values)

             keys = item['attributes'].keys()
             keys.insert(0,'entity_sample_id')
             keys.insert(0,'project')
             keys_file_samples.append(keys)
             print("File sample keys", keys)
 
        participants = get_entities(NAMESPACE,workspace,"participant")
        
        for item in participants:
             values_participants.append(item['name'])
     
        print("Participant values",values_participants)
        
       
    return values_file_samples, keys_file_samples, values_participants

if __name__ == "__main__":
    get_all_workspace_data()
