
# Schema for firecloud api to graphql

import json

import graphene
from graphene.types import generic

import utilities
import query_firecloud
from database import data

## Temp utility schema functions ##

def filter_noauth(data):
    # until we have auth setup, filter out those items that
    # we would never want to serve without authentication

    # search for two cases
    try:
        hits = data["viewer"]["repository"]["cases"]["hits"]["edges"]
        data["viewer"]["repository"]["cases"]["hits"]["edges"] = []
    except KeyError:
        pass

    try:
        hits = data["viewer"]["repository"]["samples"]["hits"]["edges"]
        data["viewer"]["repository"]["samples"]["hits"]["edges"] = []
    except KeyError:
        pass

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

class Demographic(graphene.ObjectType):
    age = graphene.String()
    weight = graphene.String()
    met = graphene.String()

class CaseSample(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    sample_id = graphene.String()
    week = graphene.String()
    time = graphene.String()
    fat = graphene.String()
    fiber = graphene.String()
    iron = graphene.String()
    alcohol = graphene.String()

class FileCase(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    project = graphene.Field(Project)
    demographic = graphene.Field(Demographic)
    primary_site = graphene.String()

    samples = graphene.List(CaseSample)

class FileCaseConnection(graphene.relay.Connection):
    class Meta:
        node = FileCase

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

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
    generic_file_name = graphene.String()

    cases = graphene.Field(FileCases)

    file_id = graphene.String()
    type = graphene.String()

    def resolve_file_id(self, info):
        return self.id

    def resolve_type(self, info):
        return self.data_format

class ProjectConnection(graphene.relay.Connection):
    class Meta:
        node = Project
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class FileConnection(graphene.relay.Connection):
    class Meta:
        node = File
    total = graphene.Int()

    def resolve_total(self, info):
        return self.iterable.total

class Bucket(graphene.ObjectType):
    doc_count = graphene.Int()
    key = graphene.String()
    key_as_string = graphene.String()

    def resolve_key_as_string(self, info):
        return str(key)

class Stats(graphene.ObjectType):
    max = graphene.Int()
    min = graphene.Int()
    count = graphene.Int()

class Aggregations(graphene.ObjectType):
    buckets = graphene.List(Bucket)
    stats = graphene.Field(Stats)

class FileAggregations(graphene.ObjectType):
    data_category = graphene.Field(Aggregations)
    file_size = graphene.Field(Aggregations)
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
        all_files = data.get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        sorted_files = utilities.sort_hits(filtered_files, sort)
        return utilities.offset_hits(sorted_files, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_files = data.get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        return data.get_file_aggregations(filtered_files)

    def resolve_facets(self, info, filters=None, facets=None):
        return data.get_facets()

class CaseAggregations(graphene.ObjectType):
    demographic__age = graphene.Field(Aggregations)
    demographic__weight = graphene.Field(Aggregations)
    demographic__met = graphene.Field(Aggregations)
    primary_site = graphene.Field(Aggregations)
    project__project_id = graphene.Field(Aggregations)
    project__program__name = graphene.Field(Aggregations)
    sample__time = graphene.Field(Aggregations)
    sample__week = graphene.Field(Aggregations)
    sample__fiber = graphene.Field(Aggregations)
    sample__fat = graphene.Field(Aggregations)
    sample__iron = graphene.Field(Aggregations)
    sample__alcohol = graphene.Field(Aggregations)

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
        return len(self.iterable)

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
    file_size = graphene.Float()

class CaseFileConnection(graphene.relay.Connection):
    class Meta:
        node = CaseFile

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class CaseFiles(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(CaseFileConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

class CaseSampleConnection(graphene.relay.Connection):
    class Meta:
        node = CaseSample

    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class CaseSamples(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(CaseSampleConnection,
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
    samples = graphene.Field(CaseSamples)

    def resolve_submitter_id(self, info):
        return self.case_id

class CaseConnection(graphene.relay.Connection):
    class Meta:
        node = Case

    total = graphene.Int()

    def resolve_total(self, info):
        return self.iterable.total

class Sample(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    sample_id = graphene.String()
    primary_site = graphene.String()
    submitter_id = graphene.String()

    demographic = graphene.Field(Demographic)
    project = graphene.Field(Project)
    summary = graphene.Field(Summary)
    annotations = graphene.Field(CaseAnnotations)

    week = graphene.String()
    time = graphene.String()
    fiber = graphene.String()
    fat = graphene.String()
    iron = graphene.String()
    alcohol = graphene.String()

    files = graphene.Field(CaseFiles)

    def resolve_submitter_id(self, info):
        return self.sample_id

class SampleAggregations(graphene.ObjectType):
    demographic__age = graphene.Field(Aggregations)
    demographic__weight = graphene.Field(Aggregations)
    demographic__met = graphene.Field(Aggregations)
    primary_site = graphene.Field(Aggregations)
    project__project_id = graphene.Field(Aggregations)
    project__program__name = graphene.Field(Aggregations)
    week = graphene.Field(Aggregations)
    time = graphene.Field(Aggregations)
    fiber = graphene.Field(Aggregations)
    fat = graphene.Field(Aggregations)
    iron = graphene.Field(Aggregations)
    alcohol = graphene.Field(Aggregations)

class SampleConnection(graphene.relay.Connection):
    class Meta:
        node = Sample

    total = graphene.Int()

    def resolve_total(self, info):
        return self.iterable.total

class RepositorySamples(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(SampleConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        sort=graphene.List(Sort),
        score=graphene.String(),
        filters=FiltersArgument())
    aggregations = graphene.Field(SampleAggregations,
        filters=FiltersArgument(),
        aggregations_filter_themselves=graphene.Boolean())

    facets = graphene.types.json.JSONString(filters=FiltersArgument(),
        facets=graphene.List(graphene.String))

    def resolve_hits(self, info, first=None, score=None, offset=None, sort=None, filters=None):
        all_samples = data.get_current_samples()
        filtered_samples = utilities.filter_hits(all_samples, filters, "samples")
        sorted_samples = utilities.sort_hits(filtered_samples, sort)
        return utilities.offset_hits(sorted_samples, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_samples = data.get_current_samples()
        filtered_samples = utilities.filter_hits(all_samples, filters, "samples")
        sample_aggregations = data.get_sample_aggregations(filtered_samples)
        return sample_aggregations

    def resolve_facets(self, info, filters=None, facets=None):
        return data.get_facets()

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
        all_cases = data.get_current_cases()
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        sorted_cases = utilities.sort_hits(filtered_cases, sort)
        return utilities.offset_hits(sorted_cases, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_cases = data.get_current_cases()
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        case_aggregations = data.get_case_aggregations(filtered_cases)
        return case_aggregations

    def resolve_facets(self, info, filters=None, facets=None):
        return data.get_facets()

class Repository(graphene.ObjectType):
    files = graphene.Field(Files)
    cases = graphene.Field(RepositoryCases)
    samples = graphene.Field(RepositorySamples)

    def resolve_files(self, info):
        return data.get_current_files()

    def resolve_cases(self, info):
        return data.get_current_cases()

    def resolve_samples(self, info):
        return data.get_current_samples()

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
        projects = data.get_current_projects(filters)
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

class CartSummary(graphene.ObjectType):
    aggregations = graphene.Field(CartSummaryAggs, 
        filters=FiltersArgument())

    def resolve_aggregations(self, info, filters=None):
        return data.get_cart_file_size(filters)

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

