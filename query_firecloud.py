
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

def get_all_workspace_data():
    # search through all of the workspaces in the namespace 
    for workspace in get_workspaces(NAMESPACE):
        print("Gather data from " + workspace)
        samples = get_entities(NAMESPACE,workspace,"sample")
        sample_attributes = dict([(item['attributes']['sample'],item['attributes']) for item in samples])
        print("sample names")
        print(sample_attributes.keys())
        participants = get_entities(NAMESPACE,workspace,"participant")
        participant_names = [item['name'] for item in participants]
        print("participant names")
        print(participant_names)

if __name__ == "__main__":
    get_all_workspace_data()
