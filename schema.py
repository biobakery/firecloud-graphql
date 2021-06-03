
# Schema for firecloud api to graphql

import json

from collections import OrderedDict

import graphene
from graphene.types import generic

import utilities
import query_firecloud

## Temp utility schema functions ##

def filter_noauth(return_data,token,data):
    # if a valid token is not provided, filter out those items that
    # we would never want to serve without authentication

    FILTER_KEYS = data.participant_metadata_columns+data.sample_metadata_columns
    SUBSTITUTE = "0"

    # check if the token is for a valid user
    if data.valid_token(token):
        return return_data

    def filter_metadata(return_data):
        if not isinstance(return_data, OrderedDict):
            return None

        for key in return_data.keys():
            if isinstance(return_data[key], OrderedDict):
                filter_metadata(return_data[key])
            elif isinstance(return_data[key], list):
                for item in return_data[key]:
                    filter_metadata(item)
            elif key in FILTER_KEYS or "metadataValue" in key:
                return_data[key]=SUBSTITUTE

    filter_metadata(return_data)

def add_attributes(instance, keys, values):
    for key in keys:
        try:
            setattr(instance, key, values[key])
        except KeyError:
            continue

## Portal API ##

class Custom(graphene.ObjectType):
    pass

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
    id = graphene.String()

class CaseSample(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    sample_id = graphene.String()

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

class AggregationAnnotation(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    metadataKey = graphene.String()
    metadataTitle = graphene.String()
    metadataType = graphene.String()
    metadataValue = graphene.Field(Aggregations)

class AggregationConnection(graphene.relay.Connection):
    class Meta:
        node = AggregationAnnotation
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class MetadataAggregations(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(AggregationConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        score=graphene.String(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

class MetadataCaseAnnotation(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    metadataKey = graphene.String()
    metadataValue = graphene.String()

class MetadataCaseConnection(graphene.relay.Connection):
    class Meta:
        node = MetadataCaseAnnotation
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class MetadataCase(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(MetadataCaseConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        score=graphene.String(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    metadata_count = graphene.String()

class MetadataSampleAnnotation(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    metadataKey = graphene.String()
    metadataValue = graphene.String()

class MetadataSampleConnection(graphene.relay.Connection):
    class Meta:
        node = MetadataSampleAnnotation
    total = graphene.Int()

    def resolve_total(self, info):
        return len(self.iterable)

class MetadataSample(graphene.ObjectType):
    hits = graphene.relay.ConnectionField(MetadataSampleConnection,
        first=graphene.Int(),
        offset=graphene.Int(),
        score=graphene.String(),
        sort=graphene.List(Sort),
        filters=FiltersArgument())

    metadata_count = graphene.String()

class FileCase(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    case_id = graphene.String()
    project = graphene.Field(Project)

    metadataCase = graphene.Field(MetadataCase)

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
    file_url = graphene.String()

    cases = graphene.Field(FileCases)

    file_id = graphene.String()
    type = graphene.String()

    def resolve_file_id(self, info):
        return self.id

    def resolve_type(self, info):
        return self.data_format

    def resolve_name(self, info):
        return self.generic_file_name

    def resolve_file_name(self, info):
        return self.generic_file_name

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
        return info.context.get("files_hits_total")

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
        all_files = info.context.get("user_data").get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files")

        # set total for hits
        info.context["files_hits_total"] = len(filtered_files)

        all_files = info.context.get("user_data").get_current_files(filters=info.context.get("user_data").get_project_access_filters())
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        sorted_files = utilities.sort_hits(filtered_files, sort)
        return utilities.offset_hits(sorted_files, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_files = info.context.get("user_data").get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        return info.context.get("user_data").get_file_aggregations(filtered_files)

    def resolve_facets(self, info, filters=None, facets=None):
        return info.context.get("user_data").get_facets()

class CaseAggregations(graphene.ObjectType):

    metadataAggregations=graphene.Field(MetadataAggregations)

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
        return info.context.get("user_data").get_case_annotation()

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

    metadataCase = graphene.Field(MetadataCase)

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
        return info.context.get("cases_hits_total")

class Sample(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    sample_id = graphene.String()
    primary_site = graphene.String()
    submitter_id = graphene.String()

    metadataCase = graphene.Field(MetadataCase)

    demographic = graphene.Field(Demographic)
    project = graphene.Field(Project)
    summary = graphene.Field(Summary)
    annotations = graphene.Field(CaseAnnotations)

    metadataSample = graphene.Field(MetadataSample)

    files = graphene.Field(CaseFiles)
    cases = graphene.Field(FileCases)

    def resolve_submitter_id(self, info):
        return self.sample_id

class SampleAggregations(graphene.ObjectType):

    metadataAggregations=graphene.Field(MetadataAggregations)

    primary_site = graphene.Field(Aggregations)
    project__project_id = graphene.Field(Aggregations)
    project__program__name = graphene.Field(Aggregations)

class SampleConnection(graphene.relay.Connection):
    class Meta:
        node = Sample

    total = graphene.Int()

    def resolve_total(self, info):
        return info.context.get("samples_hits_total")

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
        all_samples = info.context.get("user_data").get_current_samples()
        filtered_samples = utilities.filter_hits(all_samples, filters, "samples")

        # set total for sample hits
        info.context["samples_hits_total"]=len(filtered_samples)

        all_samples = info.context.get("user_data").get_current_samples(filters=info.context.get("user_data").get_project_access_filters())
        filtered_samples = utilities.filter_hits(all_samples, filters, "samples")
        sorted_samples = utilities.sort_hits(filtered_samples, sort)
        return utilities.offset_hits(sorted_samples, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_samples = info.context.get("user_data").get_current_samples()
        filtered_samples = utilities.filter_hits(all_samples, filters, "samples")
        sample_aggregations = info.context.get("user_data").get_sample_aggregations(filtered_samples)
        return sample_aggregations

    def resolve_facets(self, info, filters=None, facets=None):
        return info.context.get("user_data").get_facets()

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
        all_cases = info.context.get("user_data").get_current_cases()
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")

        # set total for hits
        info.context["cases_hits_total"] = len(filtered_cases)

        # compute limited hits
        all_cases = info.context.get("user_data").get_current_cases(filters=info.context.get("user_data").get_project_access_filters())
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        sorted_cases = utilities.sort_hits(filtered_cases, sort)
        return utilities.offset_hits(sorted_cases, offset)

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        all_cases = info.context.get("user_data").get_current_cases()
        filtered_cases = utilities.filter_hits(all_cases, filters, "cases")
        case_aggregations = info.context.get("user_data").get_case_aggregations(filtered_cases)
        return case_aggregations

    def resolve_facets(self, info, filters=None, facets=None):
        return info.context.get("user_data").get_facets()

class Repository(graphene.ObjectType):
    files = graphene.Field(Files)
    cases = graphene.Field(RepositoryCases)
    samples = graphene.Field(RepositorySamples)

    def resolve_files(self, info):
        return Files(self)

    def resolve_cases(self, info):
        return RepositoryCases(self)

    def resolve_samples(self, info):
        return RepositorySamples(self)

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
        projects = info.context.get("user_data").get_current_projects(filters)
        filtered_projects = utilities.filter_hits(projects, filters, "projects")
        return filtered_projects

    def resolve_aggregations(self, info, filters=None, aggregations_filter_themselves=None):
        projects = info.context.get("user_data").get_current_projects()
        filtered_projects = utilities.filter_hits(projects, filters, "projects")
        project_aggregations = info.context.get("user_data").get_project_aggregations(filtered_projects) 
        return project_aggregations

class FileSize(graphene.ObjectType):
    value = graphene.Float()

class CartSummaryAggs(graphene.ObjectType):
    fs = graphene.Field(FileSize)

class CartSummary(graphene.ObjectType):
    aggregations = graphene.Field(CartSummaryAggs, 
        filters=FiltersArgument())

    def resolve_aggregations(self, info, filters=None):
        return info.context.get("user_data").get_cart_file_size(filters=filters)

class Root(graphene.ObjectType):
    user = graphene.Field(User)
    count = graphene.Field(Count)
    repository = graphene.Field(Repository)
    projects = graphene.Field(Projects)
    cart_summary = graphene.Field(CartSummary)

    def resolve_user(self, info):
        return info.context.get("user_data").get_user()

    def resolve_count(self, info):
        return info.context.get("user_data").get_current_counts()

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

