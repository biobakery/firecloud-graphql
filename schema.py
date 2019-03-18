
# Schema for firecloud api to graphql

import json

import graphene
from graphene.types import generic

import utilities
import query_firecloud
from database import data

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

## Portal API ##

class Sort(graphene.String):
    pass

class FiltersArgument(generic.GenericScalar):
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
    file_count = graphene.Int()
    data_category = graphene.String()

class ExperimentalStrategies(graphene.ObjectType):
    case_count = graphene.Int()
    file_count = graphene.Int()
    experimental_strategy = graphene.String()

class Summary(graphene.ObjectType):
    case_count = graphene.Int()
    file_count = graphene.Int()
    file_size = graphene.Float()

    data_categories = graphene.List(DataCategories)
    experimental_strategies = graphene.List(ExperimentalStrategies)

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
        return data.get_project(id)

class Demographic(graphene.ObjectType):
    ethnicity = graphene.String()
    gender = graphene.String()
    race = graphene.String()

class Metadata(graphene.ObjectType):
    age2012 = graphene.Int()
    totMETs1 = graphene.String()
    weightLbs = graphene.String()
    DaysSince1Jan12 = graphene.Int()
    drAlcohol = graphene.Float()
    drB12 = graphene.Float()
    drCalories = graphene.Float()
    drCarbs = graphene.Float()
    drCholine = graphene.Float()
    drFat = graphene.Float()
    drFiber = graphene.Float()
    drFolate = graphene.Float()
    drIron = graphene.Float()
    drProtein = graphene.Float()
    participant = graphene.Int()
    q2Alcohol = graphene.String()
    q2B12 = graphene.String()
    q2Calories = graphene.String()
    q2Carbs = graphene.String()
    q2Choline = graphene.String()
    q2Fat = graphene.String()
    q2Fiber = graphene.String()
    q2Folate = graphene.String()
    q2Iron = graphene.String()
    q2Protein = graphene.String()
    Time = graphene.String()
    week = graphene.Int()
    non_ribosomal_proteins = graphene.Float()
    ribosomal_Proteins = graphene.Float()


class FileCase(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    project = graphene.Field(Project)
    demographic = graphene.Field(Demographic)
    primary_site = graphene.String()

class FileCaseConnection(graphene.relay.Connection):
    class Meta:
        node = FileCase

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

class FileCases(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(FileCaseConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

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
    file_name = graphene.String()

    cases = graphene.Field(FileCases)

    file_id = graphene.String()
    type = graphene.String()

    def resolve_file_id(self, info):
        return self.name

    def resolve_type(self, info):
        return self.data_format

    @classmethod
    def get_node(cls, info, id):
        return data.get_file(id)

class ProjectConnection(graphene.relay.Connection):
    class Meta:
        node = Project
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

class FileConnection(graphene.relay.Connection):
    class Meta:
        node = File
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

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
        score=graphene.String(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    facets = graphene.types.json.JSONString(filters=FiltersArgument(), 
        facets=graphene.List(graphene.String))
    aggregations = graphene.Field(FileAggregations, 
        filters=FiltersArgument(),
        aggregations_filter_themselves=graphene.Boolean())

    def resolve_hits(self, info, first=None, score=None, offset=None, sort=None, filters=None):
        all_files = [data.get_file(file_id) for file_id in self.hits]
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        sorted_files = utilities.sort_hits(filtered_files, sort)
        return sorted_files

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_files = [data.get_file(file_id) for file_id in self.hits]
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        return data.get_file_aggregations(filtered_files)

    def resolve_facets(self, info, filters=None, facets=None):
        return data.get_facets()

class CaseAggregations(graphene.ObjectType):
    demographic__ethnicity = graphene.Field(Aggregations)
    demographic__gender = graphene.Field(Aggregations)
    demographic__race = graphene.Field(Aggregations)
    primary_site = graphene.Field(Aggregations)
    project__project_id = graphene.Field(Aggregations)
    project__program__name = graphene.Field(Aggregations)

class CaseAnnotation(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)
    annotation_id = graphene.String()

    def resolve_annotation_id(self, info):
        return self.id

class CaseAnnotationConnection(graphene.relay.Connection):
    class Meta:
        node = CaseAnnotation
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

class CaseAnnotations(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(CaseAnnotationConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        score=graphene.String(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    def resolve_hits(self, info, first=None, score=None, offset=None, sort=None, filters=None):
        # filters are not currently in use
        return data.get_case_annotation()

class CaseFile(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    experimental_strategy = graphene.String()
    data_category = graphene.String()
    data_format = graphene.String()
    platform = graphene.String()
    access = graphene.String()

class CaseFileConnection(graphene.relay.Connection):
    class Meta:
        node = CaseFile

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

class CaseFiles(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(CaseFileConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

class Case(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    primary_site = graphene.String()
    submitter_id = graphene.String()

    demographic = graphene.Field(Demographic)
    project = graphene.Field(Project)
    summary = graphene.Field(Summary)
    annotations = graphene.Field(CaseAnnotations)

    files = graphene.Field(CaseFiles)

    def resolve_submitter_id(self, info):
        return self.case_id

class CaseConnection(graphene.relay.Connection):
    class Meta:
        node = Case

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.edges)

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

    facets = graphene.types.json.JSONString(filters=FiltersArgument(),
        facets=graphene.List(graphene.String))

    def resolve_hits(self, info, first=None, score=None, offset=None, sort=None, filters=None):
        all_cases = [data.get_case(case_id) for case_id in self.hits]
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        sorted_cases = utilities.sort_hits(filtered_cases, sort)
        return sorted_cases

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_cases = [data.get_case(case_id) for case_id in self.hits]
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        case_aggregations = data.get_case_aggregations(filtered_cases)
        return case_aggregations

    def resolve_facets(self, info, filters=None, facets=None):
        return data.get_facets()

class Repository(graphene.ObjectType):
    files = graphene.Field(Files)
    cases = graphene.Field(RepositoryCases)

    def resolve_files(self, info):
        return data.get_current_files()

    def resolve_cases(self, info):
        return data.get_current_cases()

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
        projects = data.get_current_projects()
        filtered_projects = utilities.filter_hits(projects, filters, "projects")
        return filtered_projects

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        projects = data.get_current_projects()
        filtered_projects = utilities.filter_hits(projects, filters, "projects")
        project_aggregations = data.get_project_aggregations(filtered_projects) 
        return project_aggregations

class FileSize(graphene.ObjectType):
    value = graphene.Float()

class CartSummaryAggs(graphene.ObjectType):
    fs = graphene.Field(FileSize)

    def resolve_fs(self, info):
        return data.get_cart_file_size()

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
        return data.get_user()

    def resolve_count(self, info):
        return data.get_current_counts()

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
        json_result = query_firecloud.call_api(url)
        obj_result = utilities.json2obj(json.dumps(json_result))
        return obj_result

    def resolve_samples(self, info, namespace, workspace):
        url = "workspaces/{0}/{1}/entities/{type}".format(namespace, workspace, "sample")
        json_result = query_firecloud.call_api(url)
        obj_result = utilities.json2obj(json.dumps(json_result))
        return obj_result
     

