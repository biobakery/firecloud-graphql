
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

class Program(graphene.ObjectType):
    name = graphene.String()
    program_id = graphene.String()
    id = graphene.String()

    def resolve_program_id(self, info):
        return self.name

    def resolve_id(self, info):
        return self.name

class Summary(graphene.ObjectType):
    case_count = graphene.Int()
    file_count = graphene.Int()

class Project(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    project_id = graphene.String()
    name = graphene.String()
    program = graphene.Field(Program)
    summary = graphene.Field(Summary)

    @classmethod
    def get_node(cls, info, id):
        return get_project(id)

CURRENT_PROGRAMS = [Program(name="NHSII")]

CURRENT_PROJECTS = {
    "1":Project(id="1", project_id="NHSII-DemoA", name="NHSII-DemoA", program=CURRENT_PROGRAMS[0], summary=Summary(case_count=5, file_count=15)),
    "2":Project(id="2", project_id="NHSII-DemoB", name="NHSII-DemoB", program=CURRENT_PROGRAMS[0], summary=Summary(case_count=5, file_count=15)),
    "3":Project(id="3", project_id="NHSII-DemoC", name="NHSII-DemoC", program=CURRENT_PROGRAMS[0], summary=Summary(case_count=5, file_count=15)),
} 

def get_project(id):
    return CURRENT_PROJECTS[id]

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
    projects="3",
    participants="15",
    samples="15",
    dataFormats="3",
    rawFiles="15",
    processedFiles="30"
)

class ProjectConnection(graphene.relay.Connection):
    class Meta:
        node = Project
    total = graphene.Int()

    def resolve_total(self, info):
        return len(CURRENT_PROJECTS.keys())

class FileConnection(graphene.relay.Connection):
    class Meta:
        node = File

class Files(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(FileConnection, 
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.String(),
        filters=graphene.String())

    def resolve_hits(self, info, first=None, offset=None, sort=None, filters=None):
        return [get_file(file_id) for file_id in self.hits]

class Repository(graphene.ObjectType):
    files = graphene.Field(Files)

    def resolve_files(self, info):
        return Files(hits=["1","2","3","4"])

class Bucket(graphene.ObjectType):
    doc_count = graphene.Int()
    key = graphene.String()
    key_as_string = graphene.String()

    def resolve_key_as_string(self, info):
        return str(key)

class Aggregations(graphene.ObjectType):
    buckets = graphene.List(Bucket)


PROJECT_AGGREGATIONS={
    "primary_site": Aggregations(buckets=[Bucket(doc_count=45, key="Stool")]),
    "program__name": Aggregations(buckets=[Bucket(doc_count=45, key="NHSII")]),
    "project_id": Aggregations(buckets=[Bucket(doc_count=15, key="NHSII-DemoA"),
                   Bucket(doc_count=15, key="NHSII-DemoB"),
                   Bucket(doc_count=15, key="NHSII-DemoC")]),
    "summary__data_categories__data_category": Aggregations(buckets=[Bucket(doc_count=15, key="Raw Reads"),
                                                Bucket(doc_count=15, key="Gene Families"),
                                                Bucket(doc_count=15, key="Taxonomic Profiles")]),
    "summary__experimental_strategies__experimental_strategy": Aggregations(buckets=[Bucket(doc_count=30, key="WMGX"),
                                                                Bucket(doc_count=15, key="16S")]),
}


class ProjectAggregations(graphene.ObjectType):
    primary_site = graphene.Field(Aggregations)
    program__name = graphene.Field(Aggregations)
    project_id = graphene.Field(Aggregations)
    summary__experimental_strategies__experimental_strategy = graphene.Field(Aggregations)
    summary__data_categories__data_category = graphene.Field(Aggregations)

    def resolve_primary_site(self, info):
       return PROJECT_AGGREGATIONS["primary_site"]
    def resolve_program__name(self, info):
       return PROJECT_AGGREGATIONS["program__name"]
    def resolve_project_id(self, info):
       return PROJECT_AGGREGATIONS["project_id"]
    def resolve_summary__experimental_strategies__experimental_strategy(self, info):
       return PROJECT_AGGREGATIONS["summary__experimental_strategies__experimental_strategy"]
    def resolve_summary__data_categories__data_category(self, info):
       return PROJECT_AGGREGATIONS["summary__data_categories__data_category"]

class Sort(graphene.String):
    pass

class FiltersArgument(graphene.types.json.JSONString):
    pass

class Projects(graphene.ObjectType):
    aggregations = graphene.Field(ProjectAggregations, 
        filters=FiltersArgument(),
        aggregations_filter_themselves=graphene.Boolean())
    hits = graphene.relay.ConnectionField(ProjectConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    def resolve_hits(self, info, first=None, offset=None, sort=None, filters=None):
        return [get_project(project_id) for project_id in CURRENT_PROJECTS.keys()]

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        return ProjectAggregations(self)

class Root(graphene.ObjectType):
    user = graphene.Field(User)
    count = graphene.Field(Count)
    repository = graphene.Field(Repository)
    projects = graphene.Field(Projects)

    def resolve_user(self, info):
        return User(username="null")

    def resolve_count(self, info):
        return CURRENT_COUNTS

    def resolve_repository(self, info):
        return Repository(self)

    def resolve_projects(self, info):
        return Projects(self)

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
     
