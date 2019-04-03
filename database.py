# Calls to obtain values from  database

import mysql.connector
from mysql.connector import pooling
import os
import schema
import dbqueries


# increments key for aggregations
def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):

    def __init__(self):

        self.conn_pool=mysql.connector.connect(use_pure=False, pool_name="portal",
                                                 pool_size=15,
                                                 pool_reset_session=True,
                                                 database='portal_ui',
                                                 user='biom_mass',
                                                 password=os.environ['BIOM_MASS'])
        # holds projects info
        self.projects={}

    def __exit__(self):
        try:
            self.conn_pool.close()
        except:
            print("No connection to close")

    # get connection from pool
    def get_pool(self):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        return conn, cursor

    # release connection back to pool
    def release_pool(self,conn,cursor):
        cursor.close()
        conn.close()



    #  runs query and returns result
    def fetch_results(self,cursor,query):
        cursor.execute(query)
        return [row for row in cursor]


    # get all projects from db
    def get_current_projects(self):
        conn,cursor=self.get_pool()
        projects_data=self.fetch_results(cursor,dbqueries.projects_query)
        project_object=[]
        for project in projects_data:
           getproject=self.get_project(project['id'],cursor)
           self.projects[str(project['id'])]=getproject
           project_object.append(getproject)
        self.release_pool(conn,cursor)
        return project_object

    # get user (currently none)
    def get_user(self):
        return schema.User(username="null")

    # get current version from db
    def get_current_version(self):
       conn,cursor=self.get_pool()
       version_data=self.fetch_results(cursor,dbqueries.version_query)
       self.release_pool(conn,cursor)
       del  version_data[0]['updated']
       del  version_data[0]['id']
       return version_data[0]


    # get project object details from db
    def get_project(self,id,cursor):

        project_data=self.fetch_results(cursor,dbqueries.project_query(id))
        project_id=project_data[0]['project_id']
        proj_counts_data=self.fetch_results(cursor,dbqueries.project_counts_query(project_id))

        return schema.Project(
                id=id,
                project_id=project_id,
                name=project_data[0]['name'],
                program=schema.Program(name=project_data[0]['program']),
                summary=schema.Summary(
                    case_count=proj_counts_data[1]['total'],
                    file_count=proj_counts_data[0]['total'],
                    data_categories=self.get_data_categories("project",project_id,cursor),
                    experimental_strategies=self.get_experimental_strategies("project",project_id,cursor),
                    file_size=proj_counts_data[2]['total']),
                primary_site=[project_data[0]['primary_site']])


    # get data categories file and case counts from db for a project or a participant
    def get_data_categories(self,table,id,cursor):

        data_cat_data=self.fetch_results(cursor,dbqueries.data_cat_query(table,id))
        data_cat=[]
        for item in data_cat_data:
            count_data=self.fetch_results(cursor,dbqueries.data_cat_counts_query(table,id,item['data_category']))

            data_cat.append(
                    schema.DataCategories(
                        case_count=count_data[1]['total'],
                        file_count=count_data[0]['total'],
                        data_category=item['data_category']))

        return data_cat


    # get experimental strategies file count from db for a project
    def get_experimental_strategies(self,table,id,cursor):

        exp_str_data=self.fetch_results(cursor,dbqueries.exp_str_query(table,id))
        exp_str=[]
        for item in exp_str_data:
            count_data=self.fetch_results(cursor,dbqueries.exp_str_counts_query(table,id,item['experimental_strategy']))
            exp_str.append(
                schema.ExperimentalStrategies(
                    case_count=count_data[1]['total'],
                    file_count=count_data[0]['total'],
                    experimental_strategy=item['experimental_strategy']))


        return exp_str


   # get details of file object from db
    def get_file(self,id):

        conn,cursor=self.get_pool()
        file_data=self.fetch_results(cursor,dbqueries.file_query(id))

        file_object=schema.File(
                id=id,
                name=file_data[0]['file_name'],
                participant=file_data[0]['participant'],
                sample=file_data[0]['sample'],
                access=file_data[0]['access'],
                file_size=file_data[0]['file_size'],
                data_category=file_data[0]['data_category'],
                data_format=file_data[0]['data_format'],
                platform=file_data[0]['platform'],
                experimental_strategy=file_data[0]['experimental_strategy'],
                file_name=file_data[0]['file_name'],
                cases=schema.FileCases(
                      hits=[schema.FileCase(
                      file_data[0]['part_id'],
                      case_id=file_data[0]['participant'],
                      project=self.projects[str(file_data[0]['p_id'])],
                      demographic=schema.Demographic("not hispanic or latino","male","white"),
                      metadata_participant=schema.MetadataParticipant(
                          file_data[0]['part_id'],
                          file_data[0]['participant'],
                          file_data[0]['age_2012'],
                          file_data[0]['totMETs1'],
                          file_data[0]['weight_lbs']),
                      primary_site=file_data[0]['primary_site'])]),
                file_id=file_data[0]['file_id'])

        self.release_pool(conn,cursor)
        return  file_object


    # get annotations (currently not in use)
    def get_case_annotation(self):
        return schema.CaseAnnotation()

    # get ids of all files from db
    def get_current_files(self):
        conn,cursor=self.get_pool()
        files_data=self.fetch_results(cursor,dbqueries.files_query)
        self.release_pool(conn,cursor)
        return schema.Files(hits=[file['id'] for file in files_data])

    # get ids of all cases from db
    def get_current_cases(self):
        conn,cursor=self.get_pool()
        cases_data=self.fetch_results(cursor, dbqueries.cases_query)
        self.release_pool(conn,cursor)
        return schema.RepositoryCases(hits=[case['id'] for case in cases_data])

    # get details of case object from db
    def get_case(self,id):

        # get entity_participant_id and file info from db
        conn,cursor=self.get_pool()
        case_data=self.fetch_results(cursor,dbqueries.case_query(id))
        part_id=case_data[0]['entity_participant_id']
        counts_data=self.fetch_results(cursor,dbqueries.case_counts_query(part_id))
        proj_data=self.fetch_results(cursor,dbqueries.case_project_query(part_id))
        proj_id=proj_data[0]['p_id']

        # query to get metadata from prticipant table
        metadata_part_data=self.fetch_results(cursor,dbqueries.metadata_part_query(part_id))
        del metadata_part_data[0]['updated']
        metadata_part_data[0]['participant'] = metadata_part_data[0]['entity_participant_id']
        del metadata_part_data[0]['entity_participant_id']
        metadata_participant=schema.MetadataParticipant(**metadata_part_data[0])


       # query to get metadata from sample table
        metadata_data=self.fetch_results(cursor,dbqueries.metadata_sample_query(part_id))
        metadata_list=[]
        for metadata in metadata_data:
            del metadata['updated']
            metadata_list.append(schema.MetadataSample(**metadata))

        # create file hits list
        case_files_list=[]
        for case_file in case_data:
            del case_file['entity_participant_id']
            case_files_list.append(schema.CaseFile(**case_file))

        case_object=schema.Case(id,
                    case_id=part_id,
                    primary_site=proj_data[0]['primary_site'],
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    metadata_participant=metadata_participant,
                    metadata_sample=metadata_list,
                    project=self.projects[str(proj_id)],
                    summary=schema.Summary(
                      case_count=counts_data[0]['total'],
                      file_count=counts_data[1]['total'],
                      file_size=counts_data[2]['total'],
                      data_categories=self.get_data_categories("participant",part_id,cursor),
                      experimental_strategies=self.get_experimental_strategies("participant",part_id,cursor)),
                    files=schema.CaseFiles(hits=case_files_list))


        self.release_pool(conn,cursor)
        return case_object


    def get_project_aggregations(self, projects):

        # compile aggregations from project
        aggregates = {"primary_site": {}, "program__name": {},
                      "project_id": {},
                      "summary__data_categories__data_category": {},
                      "summary__experimental_strategies__experimental_strategy": {}}

        for project in projects:
            add_key_increment(aggregates["primary_site"],project.primary_site[0])
            add_key_increment(aggregates["project_id"], project.project_id)
            add_key_increment(aggregates["program__name"], project.program.name)
            for item in project.summary.data_categories:
                add_key_increment(aggregates["summary__data_categories__data_category"], item.data_category)
            for item in project.summary.experimental_strategies:
                add_key_increment(aggregates["summary__experimental_strategies__experimental_strategy"], item.experimental_strategy)

        project_aggregates=schema.ProjectAggregations(
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project_id"].items()]),
            program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["program__name"].items()]),
            summary__data_categories__data_category=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["summary__data_categories__data_category"].items()]),
            summary__experimental_strategies__experimental_strategy=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["summary__experimental_strategies__experimental_strategy"].items()]))

        return project_aggregates



    # get all  counts for front page summary from db
    def get_current_counts(self):

        conn,cursor=self.get_pool()
        counts_data=self.fetch_results(cursor,dbqueries.all_counts_query)
        self.release_pool(conn,cursor)
        return schema.Count(
                    projects=counts_data[0]['total'],
                    participants=counts_data[1]['total'],
                    samples=counts_data[2]['total'],
                    dataFormats=counts_data[3]['total'],
                    rawFiles=counts_data[4]['total'],
                    processedFiles=counts_data[5]['total'])



    def get_file_aggregations(self, files):

        # aggregate file data
        aggregates = {"data_category": {}, "experimental_strategy": {},
                      "data_format": {}, "platform": {}, "cases__primary_site": {},
                      "cases__project__project_id": {}, "cases__metadata_participant__age_2012": {},
                      "cases__metadata_participant__totMETs1": {},"cases__metadata_participant__weight_lbs": {},
                      "access": {}}

        for file in files:

            add_key_increment(aggregates["data_category"], file.data_category)
            add_key_increment(aggregates["experimental_strategy"], file.experimental_strategy)
            add_key_increment(aggregates["data_format"], file.data_format)
            add_key_increment(aggregates["platform"], file.platform)
            add_key_increment(aggregates["access"], file.access)

            project = file.cases.hits[0].project
            add_key_increment(aggregates["cases__primary_site"], project.primary_site[0])
            add_key_increment(aggregates["cases__project__project_id"], project.project_id)

            metadata_participant = file.cases.hits[0].metadata_participant
            add_key_increment(aggregates["cases__metadata_participant__age_2012"], metadata_participant.age_2012)
            add_key_increment(aggregates["cases__metadata_participant__totMETs1"], metadata_participant.totMETs1)
            add_key_increment(aggregates["cases__metadata_participant__weight_lbs"], metadata_participant.weight_lbs)

        file_aggregates = schema.FileAggregations(
            data_category=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["data_category"].items()]),
            experimental_strategy=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["experimental_strategy"].items()]),
            data_format=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["data_format"].items()]),
            platform=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["platform"].items()]),
            cases__primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["cases__primary_site"].items()]),
            access=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["access"].items()]),
            cases__project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["cases__project__project_id"].items()]))

        return file_aggregates



    def get_case_aggregations(self, cases):

        # aggregate case data
        aggregates = {"demographic__ethnicity": {}, "demographic__gender": {},
                      "metadata_participant__age_2012": {}, "metadata_participant__totMETs1": {},
                      "metadata_participant__weight_lbs": {},
                      "demographic__race": {}, "primary_site": {}, "project__project_id": {},
                      "project__program__name": {}}

        for case in cases:
            add_key_increment(aggregates["demographic__ethnicity"], case.demographic.ethnicity)
            add_key_increment(aggregates["demographic__gender"], case.demographic.gender)
            add_key_increment(aggregates["demographic__race"], case.demographic.race)
            add_key_increment(aggregates["metadata_participant__age_2012"],case.metadata_participant.age_2012)
            add_key_increment(aggregates["metadata_participant__totMETs1"],case.metadata_participant.totMETs1)
            add_key_increment(aggregates["metadata_participant__weight_lbs"], case.metadata_participant.weight_lbs)
            add_key_increment(aggregates["primary_site"], case.primary_site[0])
            add_key_increment(aggregates["project__project_id"], case.project.project_id)
            add_key_increment(aggregates["project__program__name"], case.project.program.name)


        case_aggregates=schema.CaseAggregations(
            demographic__ethnicity=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__ethnicity"].items()]),
            demographic__gender=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__gender"].items()]),
            demographic__race=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__race"].items()]),
            metadata_participant__age_2012=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["metadata_participant__age_2012"].items()]),
            metadata_participant__totMETs1=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["metadata_participant__totMETs1"].items()]),
            metadata_participant__weight_lbs=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["metadata_participant__weight_lbs"].items()]),
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__project_id"].items()]),
            project__program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__program__name"].items()]))

        return case_aggregates

    # get facet (currently not in use)
    def get_facets(self):
        return "null" # this is not currently being used


    # get total size of all files
    def get_cart_file_size(self):
        conn,cursor=self.get_pool()
        file_data=self.fetch_results(cursor,dbqueries.files_size_query)
        self.release_pool(conn,cursor)
        return schema.FileSize(file_data[0]['sum_size'])

    def get_files_total(self):
        conn,cursor=self.get_pool()
        files_count_data=self.fetch_results(cursor,dbqueries.files_total_query)
        self.release_pool(conn,cursor)
        return files_count_data[0]['total']

    def get_cases_total(self):
        conn,cursor=self.get_pool()
        cases_count_data=self.fetch_results(cursor,dbqueries.cases_total_query)
        self.release_pool(conn,cursor)
        return cases_count_data[0]['total']

data = Data()

