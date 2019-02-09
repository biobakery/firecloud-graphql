
# Schema for firecloud api to graphql

import json

import graphene
from firecloud import api

import utilities
import data


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
        return data.get_count("projects")
    def resolve_participants(self, info):
        return data.get_count("participants")
    def resolve_samples(self, info):
        return data.get_count("samples")
    def resolve_dataFormats(self, info):
        return data.get_count("dataFormats")
    def resolve_rawFiles(self, info):
        return data.get_count("rawFiles")
    def resolve_processedFiles(self, info):
        return data.get_count("processedFiles")

class User(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    username = graphene.String()

    def resolve_username(self, info):
        return data.get_username()

    @classmethod
    def get_node(cls, info, id):
        # not currently used (needed if query is by node number)
        return User(id="1",username="null")

class File(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    participant = graphene.String()
    sample = graphene.String()
    type = graphene.String()
    raw = graphene.String()
    access = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        return get_file(id)

TEST_FILES = {
    "1": File(1, "demo_A1.fastq","person1","sample1","fastq", "raw", "open"),
    "2": File(2, "demo_A2.fastq","person2","sample2","fastq", "raw", "open"),
    "3": File(3, "demo_B1.fastq","person1B","sample1B","fastq", "raw", "open"),
    "4": File(4, "demo_B2.fastq","person2B","sample2B","fastq", "raw", "open")
}

def get_file(id):
    return TEST_FILES[id]

class FileConnection(graphene.relay.Connection):
    class Meta:
        node = File

class Repository(graphene.ObjectType):
    
    files = graphene.relay.ConnectionField(FileConnection)

    def resolve_files(self, info):
        return [get_file(file_id) for file_id in self.files]

class Root(graphene.ObjectType):

    user = graphene.Field(User)
    count = graphene.Field(Count)
    repository = graphene.Field(Repository)

    def resolve_user(self, info):
        return User(self, info)

    def resolve_count(self, info):
        return Count(self, info)

    def resolve_repository(self, info):
        return Repository(files=["1","2","3","4"])

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
     
