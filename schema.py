
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

class Count(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    projects = graphene.String()
    participants = graphene.String()
    samples = graphene.String()
    dataFormats = graphene.String()
    rawFiles = graphene.String()
    processedFiles = graphene.String()

    def resolve_projects(self, info):
        return "2"
    def resolve_participants(self, info):
        return "10"
    def resolve_samples(self, info):
        return "30"
    def resolve_dataFormats(self, info):
        return "2"
    def resolve_rawFiles(self, info):
        return "30"
    def resolve_processedFiles(self, info):
        return "90"

class User(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    username = graphene.String()

    def resolve_username(self, info):
        return "null"

    @classmethod
    def get_node(cls, info, id):
        # not currently used (needed if query is by node number)
        return User(id="1",username="null")

class Root(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    user = graphene.Field(User)
    count = graphene.Field(Count)

    def resolve_user(self, info):
        return User(self, info)

    def resolve_count(self, info):
        return Count(self, info)

def query_firecloud(url):
    """ Use the api to query firecloud """

    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()

class Query(graphene.ObjectType):

    viewer = graphene.Field(Root)
    node = graphene.relay.Node.Field()

    def resolve_viewer(self, info):
        return Root(self,info)

    entities_with_type = graphene.List(entitiesWithType, namespace=graphene.ID(required=True), workspace=graphene.ID(required=True))

    samples = graphene.List(entity, namespace=graphene.ID(required=True), workspace=graphene.ID(required=True))

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
     
