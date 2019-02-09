
# Schema for firecloud api to graphql

import json

import graphene
from firecloud import api

import utilities
import data

## Firecloud API ##

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
    """ Use the firecloud api module to query firecloud """
    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()

## Portal API ##

class Count(graphene.ObjectType):
    projects = graphene.String()
    participants = graphene.String()
    samples = graphene.String()
    dataFormats = graphene.String()
    rawFiles = graphene.String()
    processedFiles = graphene.String()

class User(graphene.ObjectType):
    username = graphene.String()

    def resolve_username(self, info):
        return data.get_username()

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

def get_file(id):
    return TEST_FILES[id]

TEST_FILES = {
    "1": File(1, "demo_A1.fastq","person1","sample1","fastq", "raw", "open"),
    "2": File(2, "demo_A2.fastq","person2","sample2","fastq", "raw", "open"),
    "3": File(3, "demo_B1.fastq","person1B","sample1B","fastq", "raw", "open"),
    "4": File(4, "demo_B2.fastq","person2B","sample2B","fastq", "raw", "open")
}

CURRENT_COUNTS = Count(
    projects=data.get_count("projects"),
    participants=data.get_count("participants"),
    samples=data.get_count("samples"),
    dataFormats=data.get_count("dataFormats"),
    rawFiles=data.get_count("rawFiles"),
    processedFiles=data.get_count("processedFiles")
)

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
        return CURRENT_COUNTS

    def resolve_repository(self, info):
        return Repository(files=["1","2","3","4"])


class Query(graphene.ObjectType):

    ## Portal API ##
    viewer = graphene.Field(Root)
    node = graphene.relay.Node.Field()

    def resolve_viewer(self, info):
        return Root(self,info)

    ## Firecloud API ##
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
     
