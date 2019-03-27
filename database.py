# Calls to obtain values from  database

import mysql.connector
from mysql.connector import pooling
import os
import schema


# increments key for aggregations
def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):

    def __init__(self):
        self.conn_pool=mysql.connector.connect(use_pure=False, pool_name="portal",
                                                 pool_size=32,
                                                 pool_reset_session=True,
                                                 database='portal_ui',
                                                 user='biom_mass',
                                                 password=os.environ['BIOM_MASS'])

       # print("Use Pure is--------", use_pure)

    def __exit__(self):
        self.conn_pool.close()

    #  runs query and returns result
    def fetch_results(self,cursor,query):
        cursor.execute(query)
        return [row for row in cursor]


    # get all projects from db
    def get_current_projects(self):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        projects_data=self.fetch_results(cursor,"select id from project")
        cursor.close()
        conn.close()
        return [self.get_project(project['id']) for project in projects_data]

    # get user (currently none)
    def get_user(self):
        return schema.User(username="null")

    # get current version from db
    def get_current_version(self):
       conn = mysql.connector.connect(pool_name="portal")
       cursor = conn.cursor(buffered=True,dictionary=True)
       version_data=self.fetch_results(cursor,
                                       "select * from version order by updated desc limit 1 ")
       cursor.close()
       conn.close()
       del  version_data[0]['updated']
       del  version_data[0]['id']
       return version_data[0]


    # get project object details from db
    def get_project(self,id):

        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        project_data=self.fetch_results(cursor,
                                        "select * from project where  id =" + str(id))
        project_id=project_data[0]['project_id']

        counts_query="select count(id) as total from  file_sample where project='"+project_id+"'"
        counts_query=counts_query+" union all "
        counts_query=counts_query+"select count(distinct participant) as total from file_sample where project='"+project_id+"'"
        counts_query=counts_query+" union all "
        counts_query=counts_query+"select sum(file_size) as total from file_sample where project='"+project_id+"'"
        proj_counts_data=self.fetch_results(cursor,counts_query)
        cursor.close()
        conn.close()

        return schema.Project(
                id=id,
                project_id=project_id,
                name=project_data[0]['name'],
                program=schema.Program(name=project_data[0]['program']),
                summary=schema.Summary(
                    case_count=proj_counts_data[1]['total'],
                    file_count=proj_counts_data[0]['total'],
                    data_categories=self.get_data_categories("project",project_id),
                    experimental_strategies=self.get_experimental_strategies("project",project_id),
                    file_size=proj_counts_data[2]['total']),
                primary_site=[project_data[0]['primary_site']])


    # get data categories file and case counts from db for a project or a participant
    def get_data_categories(self,table,id):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        data_cat_data=self.fetch_results(cursor,
            "select distinct data_category from file_sample where "+ table+"='" + str(id)+"'")
        data_cat=[]
        for item in data_cat_data:
             count_query="select count(id) as total from file_sample where data_category='"+item['data_category']+"' and "+table+"='"+str(id)+"'"
             count_query=count_query+" union all "
             count_query=count_query+"select count(distinct participant) as total from file_sample where data_category='"+item['data_category']+"' and "+table+"='"+str(id)+"'"
             count_data=self.fetch_results(cursor,count_query)

             data_cat.append(
                    schema.DataCategories(
                        case_count=count_data[1]['total'],
                        file_count=count_data[0]['total'],
                        data_category=item['data_category']))

        cursor.close()
        conn.close()
        return data_cat


    # get experimental strategies file count from db for a project
    def get_experimental_strategies(self,table,id):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        exp_str_data=self.fetch_results(cursor,
            "select distinct experimental_strategy from file_sample where "+ table+"='" + str(id) +"'")
        exp_str=[]
        for item in exp_str_data:
            count_query="select count(id) as total from file_sample where experimental_strategy='"+item['experimental_strategy']+"' and "+table+"='"+str(id)+"'"
            count_query=count_query+" union all "
            count_query=count_query+ "select count(distinct participant) as total from file_sample where experimental_strategy='"+item['experimental_strategy']+"' and "+table+"='"+str(id)+"'"
            count_data=self.fetch_results(cursor,count_query)
            exp_str.append(
                schema.ExperimentalStrategies(
                    case_count=count_data[1]['total'],
                    file_count=count_data[0]['total'],
                    experimental_strategy=item['experimental_strategy']))

        cursor.close()
        conn.close()
        return exp_str


   # get details of file object from db
    def get_file(self,id):

        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        file_query='''select file_sample.*,
                      project.id as p_id, project.project_id as proj_id,project.primary_site,
                      participant.id as part_id
                      from file_sample,project,participant where file_sample.id='''+str(id)
        file_query=file_query+''' and file_sample.project=project.project_id and
                                  file_sample.participant=participant.entity_participant_id'''
        file_data=self.fetch_results(cursor,file_query)
        cursor.close()
        conn.close()

        return schema.File(
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
                      project=self.get_project(file_data[0]['p_id']),
                      demographic=schema.Demographic("not hispanic or latino","male","white"),
                      primary_site=file_data[0]['primary_site'])]),
                file_id=file_data[0]['file_id'])


    # get annotations (currently not in use)
    def get_case_annotation(self):
        return schema.CaseAnnotation()

    # get ids of all files from db
    def get_current_files(self):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        files_data=self.fetch_results(cursor,"select `id` from `file_sample`")
        cursor.close()
        conn.close()
        return schema.Files(hits=[file['id'] for file in files_data])

    # get ids of all cases from db
    def get_current_cases(self):
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        cases_data=self.fetch_results(cursor,"select id from participant")
        cursor.close()
        conn.close()
        return schema.RepositoryCases(hits=[case['id'] for case in cases_data])

    # get details of case object from db
    def get_case(self,id):

        # get entity_participant_id and file info from db
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        case_data=self.fetch_results(cursor,'''select participant.entity_participant_id, file_sample.* from participant, file_sample
             where participant.id='''+str(id)+" and file_sample.participant=participant.entity_participant_id")
        part_id=case_data[0]['entity_participant_id']

        counts_query="select count(id) as total from participant where entity_participant_id="+str(part_id)
        counts_query=counts_query+" union all "
        counts_query=counts_query+ "select count(id) as total from file_sample where participant="+str(part_id)
        counts_query=counts_query+" union all "
        counts_query= counts_query+"select sum(file_size) as total from file_sample where participant="+str(part_id)
        counts_data=self.fetch_results(cursor,counts_query)

        proj_query="select distinct file_sample.project, project.id as p_id, project.primary_site "
        proj_query=proj_query+"from file_sample, project where file_sample.participant='"
        proj_query=proj_query+str(part_id)+"' and project.project_id=file_sample.project limit 1"
        proj_data=self.fetch_results(cursor,proj_query)

        proj_id=proj_data[0]['p_id']


        # query to get metadata from prticipant table
        metadata_part_data=self.fetch_results(cursor,
            "select * from participant where entity_participant_id="+str(part_id))
        del metadata_part_data[0]['updated']
        metadata_part_data[0]['participant'] = metadata_part_data[0]['entity_participant_id']
        del metadata_part_data[0]['entity_participant_id']
        metadata_participant=schema.MetadataParticipant(**metadata_part_data[0])


       # query to get metadata from sample table
        metadata_data=self.fetch_results(cursor,
             "select * from sample where participant="+str(part_id))
        metadata_list=[]
        for metadata in metadata_data:
            del metadata['updated']
            metadata_list.append(schema.MetadataSample(**metadata))

        cursor.close()
        conn.close()

        return schema.Case(id,
                    case_id=part_id,
                    primary_site=proj_data[0]['primary_site'],
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    metadata_participant=metadata_participant,
                    metadata_sample=metadata_list,
                    project=self.get_project(proj_id),
                    summary=schema.Summary(
                      case_count=counts_data[0]['total'],
                      file_count=counts_data[1]['total'],
                      file_size=counts_data[2]['total'],
                      data_categories=self.get_data_categories("participant",part_id),
                      experimental_strategies=self.get_experimental_strategies("participant",part_id)),
                    files=schema.CaseFiles(hits=[schema.CaseFile(
                               case_file['id'],
                               experimental_strategy=case_file['experimental_strategy'],
                               data_category=case_file['data_category'],
                               data_format=case_file['data_format'],
                               platform=case_file['platform'],
                               access=case_file['access']) for case_file in case_data]))



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

        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        counts_data=self.fetch_results(cursor,'''select count(id) as countid from project
                               union all select count(id) as countid from participant
                               union all select count(id) as countid from sample
                               union all select count(distinct data_format) as countid from file_sample
                               union all select count(id) as countid from file_sample where  type="rawFiles"
                               union all select count(id) as countid from file_sample where type="processedFiles"''')
        cursor.close()
        conn.close()
        return schema.Count(
                    projects=counts_data[0]['countid'],
                    participants=counts_data[1]['countid'],
                    samples=counts_data[2]['countid'],
                    dataFormats=counts_data[3]['countid'],
                    rawFiles=counts_data[4]['countid'],
                    processedFiles=counts_data[5]['countid'])



    def get_file_aggregations(self, files):

        # aggregate file data
        aggregates = {"data_category": {}, "experimental_strategy": {},
                      "data_format": {}, "platform": {}, "cases__primary_site": {},
                      "cases__project__project_id": {}, "access": {}}

        for file in files:

            add_key_increment(aggregates["data_category"], file.data_category)
            add_key_increment(aggregates["experimental_strategy"], file.experimental_strategy)
            add_key_increment(aggregates["data_format"], file.data_format)
            add_key_increment(aggregates["platform"], file.platform)
            add_key_increment(aggregates["access"], file.access)

            project = file.cases.hits[0].project
            add_key_increment(aggregates["cases__primary_site"], project.primary_site[0])
            add_key_increment(aggregates["cases__project__project_id"], project.project_id)

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
        conn = mysql.connector.connect(pool_name="portal")
        cursor = conn.cursor(buffered=True,dictionary=True)
        file_data=self.fetch_results(cursor,"select sum(file_size) as sum_size from  file_sample")
        cursor.close()
        conn.close()
        return schema.FileSize(file_data[0]['sum_size'])

data = Data()

VERSION = data.get_current_version()
