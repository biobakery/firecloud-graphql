
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

class Sort(graphene.String):
    pass

class FiltersArgument(graphene.types.json.JSONString):
    pass

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

class DataCategories(graphene.ObjectType):
    case_count = graphene.Int()
    data_category = graphene.String()

class Summary(graphene.ObjectType):
    case_count = graphene.Int()
    file_count = graphene.Int()
    file_size = graphene.Float()

    data_categories = graphene.List(DataCategories)

class Project(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    project_id = graphene.String()
    name = graphene.String()
    program = graphene.Field(Program)
    summary = graphene.Field(Summary)
    primary_site = graphene.List(graphene.String)

    @classmethod
    def get_node(cls, info, id):
        return get_project(id)

class FileCase(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    project = graphene.Field(Project)

class FileCaseConnection(graphene.relay.Connection):
    class Meta:
        node = FileCase

    total = graphene.Int()

    def resolve_total(self, info):
        return get_total_cases_per_file()

class FileCases(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(FileCaseConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    def resolve_hits(self, info, first=None, offset=None, sort=None, filters=None):
        return [get_filecase(file_id) for file_id in self.hits]

class File(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    participant = graphene.String()
    sample = graphene.String()
    access = graphene.String()
    file_size = graphene.Float()
    data_category = graphene.String()
    data_format = graphene.String()
    platform = graphene.String()
    experimental_strategy = graphene.String()

    cases = graphene.Field(FileCases)

    file_id = graphene.String()
    file_name = graphene.String()
    type = graphene.String()

    def resolve_file_id(self, info):
        return self.name

    def resolve_file_name(self, info):
        return self.name

    def resolve_type(self, info):
        return self.data_format

    @classmethod
    def get_node(cls, info, id):
        return get_file(id)

class ProjectConnection(graphene.relay.Connection):
    class Meta:
        node = Project
    total = graphene.Int()

    def resolve_total(self, info):
        return get_total_projects_count()

class FileConnection(graphene.relay.Connection):
    class Meta:
        node = File
    total = graphene.Int()

    def resolve_total(self, info):
        return get_total_files()

class Bucket(graphene.ObjectType):
    doc_count = graphene.Int()
    key = graphene.String()
    key_as_string = graphene.String()

    def resolve_key_as_string(self, info):
        return str(key)

class Aggregations(graphene.ObjectType):
    buckets = graphene.List(Bucket)

class FileAggregations(graphene.ObjectType):
    data_category = graphene.Field(Aggregations)
    experimental_strategy = graphene.Field(Aggregations)
    data_format = graphene.Field(Aggregations)
    platform = graphene.Field(Aggregations)
    access = graphene.Field(Aggregations)
    cases__project__project_id = graphene.Field(Aggregations)
    cases__primary_site = graphene.Field(Aggregations)

class Files(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(FileConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    facets = graphene.types.json.JSONString(filters=FiltersArgument(), 
        facets=graphene.List(graphene.String))
    aggregations = graphene.Field(FileAggregations, 
        filters=FiltersArgument(),
        aggregations_filter_themselves=graphene.Boolean())

    def resolve_hits(self, info, first=None, offset=None, sort=None, filters=None):
        return [get_file(file_id) for file_id in self.hits]

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        return get_file_aggregations()

    def resolve_facets(self, info, filters=None, facets=None):
        return get_file_facets()

class CaseAggregations(graphene.ObjectType):
    demographic__ethnicity = graphene.Field(Aggregations)
    demographic__gender = graphene.Field(Aggregations)
    demographic__race = graphene.Field(Aggregations)
    primary_site = graphene.Field(Aggregations)
    project__project_id = graphene.Field(Aggregations)
    project__program__name = graphene.Field(Aggregations)

class CaseFile(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    acl = graphene.String()
    file_name = graphene.String()

class CaseConnection(graphene.relay.Connection):
    class Meta:
        node = CaseFile

    total = graphene.Int()

    def resolve_total(self, info):
        return get_total_cases_per_file()

class RepositoryCases(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(CaseConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        score=graphene.String(),
        filters=FiltersArgument())
    aggregations = graphene.Field(CaseAggregations,
        filters=FiltersArgument(),
        aggregations_filter_themselves=graphene.Boolean())

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        return get_case_aggregations()

class Repository(graphene.ObjectType):
    files = graphene.Field(Files)
    cases = graphene.Field(RepositoryCases)

    def resolve_files(self, info):
        return get_current_files()

class ProjectAggregations(graphene.ObjectType):
    primary_site = graphene.Field(Aggregations)
    program__name = graphene.Field(Aggregations)
    project_id = graphene.Field(Aggregations)
    summary__experimental_strategies__experimental_strategy = graphene.Field(Aggregations)
    summary__data_categories__data_category = graphene.Field(Aggregations)

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
        return get_project_aggregations()

class FileSize(graphene.ObjectType):
    value = graphene.Float()

class CartSummaryAggs(graphene.ObjectType):
    fs = graphene.Field(FileSize)

    def resolve_fs(self, info):
        return get_cart_file_size()

class CartSummary(graphene.ObjectType):
    aggregations = graphene.Field(CartSummaryAggs, 
        filters=FiltersArgument())

class Root(graphene.ObjectType):
    user = graphene.Field(User)
    count = graphene.Field(Count)
    repository = graphene.Field(Repository)
    projects = graphene.Field(Projects)
    cart_summary = graphene.Field(CartSummary)

    def resolve_user(self, info):
        return get_user()

    def resolve_count(self, info):
        return get_current_counts()

    def resolve_repository(self, info):
        return Repository(self)

    def resolve_projects(self, info):
        return Projects(self)

    def resolve_cart_summary(self, info):
        return CartSummary(self)

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
     
# Constants
def get_total_projects_count():
    return len(CURRENT_PROJECTS.keys())

def get_user():
    return User(username="null") # no users are currently being used

def get_filecase(id):
    return CURRENT_FILE_CASES[id]

def get_project(id):
    return CURRENT_PROJECTS[id]

def get_file(id):
    return TEST_FILES[id]

def get_total_files():
    return len(CURRENT_FILES.hits)

def get_current_files():
    return CURRENT_FILES

def get_project_aggregations():
    return PROJECT_AGGREGATIONS

def get_current_counts():
    return CURRENT_COUNTS

def get_file_aggregations():
    return FILE_AGGREGATIONS

def get_case_aggregations():
    return CASE_AGGREGATIONS

def get_total_cases_per_file():
    return 1 # there is always at most one case per file

def get_file_facets():
    return "null" # this is not currently being used

def get_cart_file_size():
    return FileSize(65000000000) # this is the total amount of files in repo table shown

CURRENT_PROGRAMS = [Program(name="NHSII")]

DATA_CATEGORIES = [DataCategories(case_count=2, data_category="Raw Reads"),
                   DataCategories(case_count=2, data_category="Gene Families"),
                   DataCategories(case_count=2, data_category="Taxonomic Profiles")]

CURRENT_PROJECTS = {
    "1":Project(id="1", project_id="NHSII-DemoA", name="NHSII-DemoA", program=CURRENT_PROGRAMS[0], summary=Summary(case_count=2, file_count=6, data_categories=DATA_CATEGORIES, file_size=15), primary_site=["Stool"]),
    "2":Project(id="2", project_id="NHSII-DemoB", name="NHSII-DemoB", program=CURRENT_PROGRAMS[0], summary=Summary(case_count=2, file_count=6, data_categories=DATA_CATEGORIES, file_size=15), primary_site=["Stool"]),
} 

CURRENT_FILE_CASES = {
    "1":FileCase(1,"Case1",get_project("1")),
    "2":FileCase(2,"Case2",get_project("1")),
    "3":FileCase(3,"Case3",get_project("2")),
    "4":FileCase(4,"Case4",get_project("2")),
}

FILE_SIZES = { "gene": 300000000, "raw": 5000000000, "taxa": 200000000 }

TEST_FILES = {
    "1": File(1, "demoA_sample1_raw_reads.fastq","case1","sample1", "controlled", FILE_SIZES["raw"], "Raw Reads", "Illumina", "Fastq", "WMGX", FileCases(hits=["1"])),
    "2": File(2, "demoA_sample1_taxonomic_profile.tsv","case1","sample1", "open", FILE_SIZES["taxa"], "Taxonomic Profile", "Illumina", "TSV", "WMGX", FileCases(hits=["1"])),
    "3": File(3, "demoA_sample1_gene_families.tsv","case1","sample1", "open", FILE_SIZES["gene"], "Gene Families", "Illumina", "TSV", "WMGX", FileCases(hits=["1"])),
    "4": File(4, "demoA_sample2_raw_reads.fastq","case2","sample2", "controlled", FILE_SIZES["raw"], "Raw Reads", "Illumina", "Fastq", "WMGX", FileCases(hits=["2"])),
    "5": File(5, "demoA_sample2_taxonomic_profile.tsv","case2","sample2", "open", FILE_SIZES["taxa"], "Taxonomic Profile", "Illumina", "TSV", "WMGX", FileCases(hits=["2"])),
    "6": File(6, "demoA_sample2_gene_families.tsv","case2","sample2", "open", FILE_SIZES["gene"], "Gene Families", "Illumina", "TSV", "WMGX", FileCases(hits=["2"])),

    "7": File(7, "demoB_sample3_raw_reads.fastq","case3","sample3", "controlled", FILE_SIZES["raw"], "Raw Reads", "Illumina", "Fastq", "WMGX", FileCases(hits=["3"])),
    "8": File(8, "demoB_sample3_taxonomic_profile.tsv","case3","sample3", "open", FILE_SIZES["taxa"], "Taxonomic Profile", "Illumina", "TSV", "WMGX", FileCases(hits=["3"])),
    "9": File(9, "demoB_sample3_gene_families.tsv","case3","sample3", "open", FILE_SIZES["gene"], "Gene Families", "Illumina", "TSV", "WMGX", FileCases(hits=["3"])),
    "10": File(10, "demoB_sample4_raw_reads.fastq","case4","sample4", "controlled", FILE_SIZES["raw"], "Raw Reads", "Illumina", "Fastq", "WMGX", FileCases(hits=["4"])),
    "11": File(11, "demoB_sample4_taxonomic_profile.tsv","case4","sample4", "open", FILE_SIZES["taxa"], "Taxonomic Profile", "Illumina", "TSV", "WMGX", FileCases(hits=["4"])),
    "12": File(12, "demoB_sample4_gene_families.tsv","case4","sample4", "open", FILE_SIZES["gene"], "Gene Families", "Illumina", "TSV", "WMGX", FileCases(hits=["4"])),
}

CURRENT_COUNTS = Count(
    projects="2",
    participants="4",
    samples="4",
    dataFormats="3",
    rawFiles="4",
    processedFiles="8"
)

CURRENT_FILES = Files(hits=TEST_FILES.keys())

FILE_AGGREGATIONS=FileAggregations(
    data_category=Aggregations(buckets=[
        Bucket(doc_count=4, key="Raw Reads"),
        Bucket(doc_count=4, key="Taxonomic Profile"),
        Bucket(doc_count=4, key="Gene Families")]),
    experimental_strategy=Aggregations(buckets=[
        Bucket(doc_count=6, key="WMGX"),
        Bucket(doc_count=6, key="16S")]),
    data_format=Aggregations(buckets=[
        Bucket(doc_count=4, key="Fastq"),
        Bucket(doc_count=8, key="TSV")]),
    platform=Aggregations(buckets=[
        Bucket(doc_count=6, key="Illumina MiSeq"),
        Bucket(doc_count=6, key="Illumina HiSeq")]),
    cases__primary_site=Aggregations(buckets=[
        Bucket(doc_count=12, key="Stool")]),
    cases__project__project_id=Aggregations(buckets=[
        Bucket(doc_count=6, key="NHSII-DemoA"),
        Bucket(doc_count=6, key="NHSII-DemoB")]),
    access=Aggregations(buckets=[
        Bucket(doc_count=4, key="open"),
        Bucket(doc_count=8, key="controlled")]))

CASE_AGGREGATIONS=CaseAggregations(
    demographic__ethnicity=Aggregations(buckets=[
        Bucket(doc_count=10, key="not hispanic or latino"),
        Bucket(doc_count=2, key="hispanic or latino")]),
    demographic__gender=Aggregations(buckets=[
        Bucket(doc_count=8, key="male"),
        Bucket(doc_count=4, key="female")]),
    demographic__race=Aggregations(buckets=[
        Bucket(doc_count=8, key="white"),
        Bucket(doc_count=4, key="asian")]),
    primary_site=Aggregations(buckets=[
        Bucket(doc_count=12, key="Stool")]),
    project__project_id=Aggregations(buckets=[
        Bucket(doc_count=6, key="NHSII-DemoA"),
        Bucket(doc_count=6, key="NHSII-DemoB")]),
    project__program__name=Aggregations(buckets=[
        Bucket(doc_count=12, key="NHSII")]),
)

PROJECT_AGGREGATIONS=ProjectAggregations(
    primary_site=Aggregations(buckets=[Bucket(doc_count=45, key="Stool")]),
    program__name=Aggregations(buckets=[Bucket(doc_count=45, key="NHSII")]),
    project_id=Aggregations(buckets=[Bucket(doc_count=15, key="NHSII-DemoA"),
                   Bucket(doc_count=15, key="NHSII-DemoB"),
                   Bucket(doc_count=15, key="NHSII-DemoC")]),
    summary__data_categories__data_category=Aggregations(buckets=[Bucket(doc_count=15, key="Raw Reads"),
                                                Bucket(doc_count=15, key="Gene Families"),
                                                Bucket(doc_count=15, key="Taxonomic Profiles")]),
    summary__experimental_strategies__experimental_strategy=Aggregations(buckets=[Bucket(doc_count=30, key="WMGX"),
                                                                Bucket(doc_count=15, key="16S")]))

