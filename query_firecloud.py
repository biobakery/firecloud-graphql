
# Code to query the firecloud api

import json 

from firecloud import api

NAMESPACE="biom-mass-firecloud-ana"
WORKSPACES=["HPFS_Demo1"]

def call_api(url):
    """ Use the firecloud api module to query firecloud 
        Allows for additional options not included in fiss api"""
    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()

def get_entities(namespace, workspace, entity_type):
    url = "workspaces/{0}/{1}/entities/{2}".format(namespace,workspace,entity_type)
    json_result = call_api(url)
    return json_result

def get_all_workspace_data():
    for workspace in WORKSPACES:
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
