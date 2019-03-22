# Calls to obtain values from  database

import mysql.connector as mariadb
import json
import schema


# increments key for aggregations
def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):

    # connects to db and runs query
    def fetch_results(self,query):

        db_conn = mariadb.connect(user='biom_mass', password='DanDa1osh', db='portal_ui')
        cursor = db_conn.cursor(buffered=True)
        cursor.execute(query)
        # response json
        row_headers=[x[0] for x in cursor.description]
        rows = cursor.fetchall()
        json_data=[]
        for row in rows:
            json_data.append(dict(zip(row_headers,row)))
        cursor.close()
        db_conn.close()

        return json_data

    # get all projects from db
    def get_current_projects(self):
        projects_json=self.fetch_results("select `id` from `project`")
        return [self.get_project(project['id']) for project in projects_json]

    # get user (currently none)
    def get_user(self):
        return schema.User(username="null")

    # get current version from db
    def get_version(self):
       version_json=self.fetch_results("select * from `version` order by updated desc limit 1 ")
       del  version_json[0]['updated']
       del  version_json[0]['id']
       return schema.Version(**version_json[0])


    # get project object details from db
    def get_project(self,id):

        project_json=self.fetch_results(
            "select * from  `project` where  `id` =" + str(id))
        project_id=project_json[0]['project_id']
        proj_id=project_json[0]['id']
        proj_name=project_json[0]['name']
        proj_program=project_json[0]['program']
        proj_primary_site=[project_json[0]['primary_site']]
        #proj_primary_site=["Stool"]

        file_count_json=self.fetch_results(
            "select count(id) as file_count from  file_sample where project='"+project_id+"'")
        proj_file_count=file_count_json[0]['file_count']

        part_count_json=self.fetch_results(
            "select count(distinct participant) as part_count from file_sample where project='"+project_id+"'")
        proj_part_count=part_count_json[0]['part_count']

        sum_file_size_json=self.fetch_results(
            "select sum(file_size) as sum_file_size from file_sample where project='"+project_id+"'")
        proj_file_size=sum_file_size_json[0]['sum_file_size']

        return schema.Project(
                id=proj_id,
                project_id=project_id,
                name=proj_name,
                program=schema.Program(name=proj_program),
                summary=schema.Summary(
                    case_count=proj_part_count,
                    file_count=proj_file_count,
                    data_categories=self.get_data_categories("project",project_id),
                    experimental_strategies=self.get_experimental_strategies("project",project_id),
                    file_size=proj_file_size),
                primary_site=proj_primary_site)


    # get data categories file and case counts from db for a project or a participant 
    def get_data_categories(self,table,id):

        data_cat_json=self.fetch_results(
            "select distinct data_category from file_sample where "+ table+"='" + str(id)+"'")
        data_cat=[]
        for item in data_cat_json:

            if table is "participant":
                item_files_json=self.fetch_results(
                   "select count(id) as file_count from file_sample where data_category='"+item['data_category']+"' and "+table+"='"+str(id)+"'")
                file_count=0
                if len(item_files_json) > 0:
                    file_count=item_files_json[0]['file_count']

                data_cat.append(
                    schema.DataCategories(
                      file_count=file_count,
                      data_category=item['data_category']))
            elif table is "project":
                item_part_json=self.fetch_results(
                   "select count(distinct participant) as case_count from file_sample where data_category='"+item['data_category']+"' and "+table+"='"+str(id)+"'")

                case_count=0
                if  len(item_part_json) > 0:
                    case_count=item_part_json[0]['case_count']
                data_cat.append(
                    schema.DataCategories(
                        case_count=case_count,
                        data_category=item['data_category']))

        return data_cat


    # get experimental strategies file count from db for a project 
    def get_experimental_strategies(self,table,id):

        exp_str_json=self.fetch_results(
            "select distinct experimental_strategy from file_sample where "+ table+"='" + str(id) +"'")

        exp_str=[]
        for item in exp_str_json:
            item_files_json=self.fetch_results(
               "select count(id) as filecount from file_sample where experimental_strategy='"+item['experimental_strategy']+"' and "+table+"='"+str(id)+"'")
#           item_part_json=self.fetch_results(
#              "select count(distinct participant) as case_count from file_sample where experimental_strategy='"+item['experimental_strategy']+"' and "+table+"='"+str(id)+"'")
#
#           case_count=0
#           if len(item_part_json) > 0:
#                case_count=item_part_json[0]['case_count']

            file_count=0
            if len(item_files_json) > 0:
                file_count=item_files_json[0]['filecount']
            exp_str.append(
                schema.ExperimentalStrategies(
#                   case_count=case_count,
                    file_count=file_count,
                   # experimental_strategy="wmgx"))
                    experimental_strategy=item['experimental_strategy']))

        return exp_str


   # get details of file object from db
    def get_file(self,id):

        file_json=self.fetch_results("select * from `file_sample` where  `id` ="+ str(id))
        project_json=self.fetch_results(
            "select id , project_id, primary_site from project where  project_id='"+file_json[0]['project']+"'")
        part_json=self.fetch_results(
           "select id, entity_participant_id from participant where  entity_participant_id='"+file_json[0]['participant']+"'")

        return schema.File(
                id=file_json[0]['id'],
                name=file_json[0]['file_name'],
                participant=file_json[0]['participant'],
                sample=file_json[0]['sample'],
                access=file_json[0]['access'],
                file_size=file_json[0]['file_size'],
                data_category=file_json[0]['data_category'],
                data_format=file_json[0]['data_format'],
                platform=file_json[0]['platform'],
                experimental_strategy=file_json[0]['experimental_strategy'],
                file_name=file_json[0]['file_name'],
                cases=schema.FileCases(
                      hits=[schema.FileCase(
                      part_json[0]['id'],
                      case_id=file_json[0]['participant'],
                      project=self.get_project(project_json[0]['id']),
                      demographic=schema.Demographic("not hispanic or latino","male","white"),
                      primary_site=project_json[0]['primary_site'])]),
                file_id=file_json[0]['file_id'])

    # get annotations (currently not in use)
    def get_case_annotation(self):
        return schema.CaseAnnotation()

    # get ids of all files from db
    def get_current_files(self):

        files_json=self.fetch_results("select `id` from `file_sample`")
        return schema.Files(hits=[item['id'] for item in files_json])

    # get ids of all cases from db
    def get_current_cases(self):

        cases_json=self.fetch_results("select id from participant")
        return schema.RepositoryCases(hits=[case['id'] for case in cases_json])

    # get details of case object from db
    def get_case(self,id):

        case_json=self.fetch_results("select * from participant where id="+str(id))
        part_id=case_json[0]['entity_participant_id']

        case_count_json=self.fetch_results(
            "select count(entity_participant_id) as case_count from participant where entity_participant_id="+str(part_id))
        case_count=case_count_json[0]['case_count']

        file_count_json=self.fetch_results(
            "select count(id) as file_count from file_sample where participant="+str(part_id))
        file_count=file_count_json[0]['file_count']

        file_size_json=self.fetch_results(
            "select sum(file_size) as filesize from file_sample where participant="+str(part_id))
        file_size=file_size_json[0]['filesize']

        proj_query="select distinct file_sample.project, project.id as proj_id "
        proj_query=proj_query+"from file_sample, project where file_sample.participant='"
        proj_query=proj_query+str(part_id)+"' and project.project_id=file_sample.project limit 1"
        proj_json=self.fetch_results(proj_query)
        proj_id=proj_json[0]['proj_id']

        # query to get files from file_sample table
        files_json=self.fetch_results("select * from file_sample where participant="+str(part_id))

        # query to get metadata from prticipant table
        metadata_part_json=self.fetch_results(
            "select * from participant where entity_participant_id="+str(part_id))

        del metadata_part_json[0]['updated']
        metadata_part_json[0]['participant'] = metadata_part_json[0]['entity_participant_id']
        del metadata_part_json[0]['entity_participant_id']
        metadata_participant=schema.MetadataParticipant(**metadata_part_json[0])


       # query to get metadata from sample table
        metadata_json=self.fetch_results("select * from sample where participant="+str(part_id))
        metadata_list=[]
        for metadata in metadata_json:
            del metadata['updated']
            metadata_list.append(schema.MetadataSample(**metadata))


        return schema.Case(id,
                    case_id=part_id,
                    primary_site="Stool",
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    metadata_participant=metadata_participant,
                    metadata_sample=metadata_list,
                    project=self.get_project(proj_id),
                    summary=schema.Summary(
                      case_count=case_count,
                      file_count=file_count,
                      file_size=file_size,
                      data_categories=self.get_data_categories("participant",part_id)),
                      #experimental_strategies=self.get_experimental_strategies("participant",part_id)),
                    files=schema.CaseFiles(hits=[schema.CaseFile(
                               case_file['id'],
                               experimental_strategy=case_file['experimental_strategy'],
                               data_category=case_file['data_category'],
                               data_format=case_file['data_format'],
                               platform=case_file['platform'],
                               access=case_file['access']) for case_file in files_json]))



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

        projects_json = self.fetch_results("select count(`project_id`)as projects_count from project")
        projects = projects_json[0]['projects_count']

        participants_json = self.fetch_results("select count(`entity_participant_id`) as participants_count from `participant`")
        participants = participants_json[0]['participants_count']

        samples_json = self.fetch_results("select count(`sample`) as samples_count from `sample`")
        samples =  samples_json[0]['samples_count']

        dataFormats_json = self.fetch_results("select count(distinct `data_format`) as data_format_count from `file_sample`")
        dataFormats = dataFormats_json[0]['data_format_count']

        rawFiles_json = self.fetch_results(
            "select count(`id`) as rawfiles_count from `file_sample` where type='rawFiles'")
        rawFiles = rawFiles_json[0]['rawfiles_count']

        prFiles_json = self.fetch_results(
            "select count(`id`) as prfiles_count from `file_sample` where type='processedFiles'")
        prFiles = prFiles_json[0]['prfiles_count']

        return schema.Count(
                    projects=projects,
                    participants=participants,
                    samples=samples,
                    dataFormats=dataFormats,
                    rawFiles=rawFiles,
                    processedFiles=prFiles)



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

        file_json=self.fetch_results("select sum(file_size) as sum_size from  file_sample")
        return schema.FileSize(file_json[0]['sum_size'])

data = Data()
