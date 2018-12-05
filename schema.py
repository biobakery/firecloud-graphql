
# Schema for firecloud api to graphql

import json

import graphene
from firecloud import api

import utilities

class Entities(graphene.ObjectType):
    namespace = graphene.ID()
    workspace = graphene.ID()
    attributes = graphene.String()

def query_firecloud(url):
    """ Use the api to query firecloud """

    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()

class Query(graphene.ObjectType):
    entities = graphene.List(Entities, namespace=graphene.ID(required=True), workspace=graphene.ID(required=True))

    def resolve_entities(self, info, namespace, workspace):
        url = "workspaces/{0}/{1}/entities_with_type".format(namespace, workspace)
        json_result = query_firecloud(url)
        obj_result = utilities.json2obj(json.dumps(json_result))
        return obj_result
