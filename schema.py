
# Schema for firecloud api to graphql

import json

import graphene
from firecloud import api

import utilities

class entitiesWithType(graphene.ObjectType):
    namespace = graphene.ID()
    workspace = graphene.ID()
    attributes = graphene.String()

class entity(graphene.ObjectType):
    namespace = graphene.ID()
    workspace = graphene.ID()
    name = graphene.String()
    entityType = graphene.String()
    attributes = graphene.String()

def query_firecloud(url):
    """ Use the api to query firecloud """

    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()

class Query(graphene.ObjectType):
    entities_with_type = graphene.List(entitiesWithType, namespace=graphene.ID(required=True), workspace=graphene.ID(required=True))

    samples = graphene.List(entity, namespace=graphene.ID(required=True), workspace=graphene.ID(required=True))
    status = graphene.List(Status)

    def resolve_entities_with_type(self, info, namespace, workspace):
        url = "workspaces/{0}/{1}/entities_with_type".format(namespace, workspace)
        json_result = query_firecloud(url)
        obj_result = utilities.json2obj(json.dumps(json_result))
        return obj_result

    def resolve_samples(self, info, namespace, workspace):
        url = "workspaces/{0}/{1}/entities/{type}".format(namespace, workspace, "sample")
        json_result = query_firecloud(url)
        obj_result = utilities.json2obj(json.dumps(json_result))
        return obj_result
     
        reviews = List(Review, id=Int(required=True))

