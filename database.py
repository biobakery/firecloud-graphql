# Calls to obtain values from  database

import mysql.connector as mariadb
import json

def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):
    db_conn = mariadb.connect(user='biom-mass', password='', db='portal_ui')
    cursor = db_conn.cursor(buffered=True)

    def fetch_results(self,query):
        self.cursor.execute(query)
        row_headers=[x[0] for x in self.cursor.description]
        rows = self.cursor.fetchall()
        json_data=[]
        for row in rows:
            json_data.append(dict(zip(row_headers,row)))
        return json_data

    def get_current_projects(self):
        projects_json=self.fetch_results("select `id` from `project`")
        print("json_data  inside get_current_projects")
        print(projects_json)
        return [self.get_project(project['id']) for project in projects_json]

    def get_user(self):
        import schema
        return schema.User(username="null")

    def get_project(self,id):
        import schema

        print("id inside get_project")
        print(id)
        project_json=self.fetch_results(
            "select id, project_id, name as pr_name, program from  `project` where  `id` =" + str(id))
        project_id=project_json[0]['project_id']
        proj_id=project_json[0]['id']
        proj_name=project_json[0]['pr_name']
        proj_program=["HPFS"]
        #proj_program=project_json[0]['program']
        #proj_primary_site=project_json[0]['primary_site']
        proj_primary_site=["Stool"]

        file_count_json=self.fetch_results("select count(id) as file_count from  file_sample where project='"+project_id+"'")
        proj_file_count=file_count_json[0]['file_count']

        part_count_json=self.fetch_results(
            "select count(distinct participant) as part_count from file_sample where project='"+project_id+"'")
        proj_part_count=part_count_json[0]['part_count']

        data_cat_json=self.fetch_results("select distinct data_category from file_sample where project='"+project_id+"'")
        proj_data_cat=[data_cat['data_category'] for  data_cat in data_cat_json]

        exp_str_json=self.fetch_results("select distinct experimental_strategy from file_sample where project='"+project_id+"'")
        proj_exp_str=[exp_str['experimental_strategy'] for exp_str in exp_str_json]

        sum_file_size_json=self.fetch_results(
            "select sum(file_size) as sum_file_size from file_sample where project='"+project_id+"'")
        proj_file_size=sum_file_size_json[0]['sum_file_size']
        print("values inside get_project")
        print(
            proj_id,project_id,proj_name,proj_program,proj_part_count,proj_file_count,proj_data_cat,proj_exp_str,proj_file_size,proj_primary_site)

        return schema.Project(
                id=proj_id,
                project_id=project_id,
                name=proj_name,
                program=proj_program,
                summary=schema.Summary(
                    case_count=proj_part_count,
                    file_count=proj_file_count,
                    data_categories=proj_data_cat,
                    experimental_strategies=proj_exp_str,
                    file_size=proj_file_size),
                primary_site=proj_primary_site)


    def get_file(self,id):
        import schema

        file_json=self.fetch_results("select * from `file_sample` where  `id` ="+ str(id))
        project_json=self.fetch_results(
            "select id , project_id, primary_site from project where  project_id='"+file_json[0]['project']+"'")
        part_json=self.fetch_results(
           "select id, entity_participant_id from participant where  entity_participant_id='"+file_json[0]['participant']+"'")
        print("file and project json inside get_file")
        print(file_json[0]['sample'])
        print(project_json[0]['project_id'])
        return schema.File(
                id=file_json[0]['id'],
                name=file_json[0]['file_name'],
                file_id=file_json[0]['file_id'],
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
                      #primary_site=project_json[0]['primary_site']
                      primary_site="Stool")]))

    def get_case_annotation(self):
        import schema
        return schema.CaseAnnotation()

    def get_current_files(self):
        import schema

        files_json=self.fetch_results("select `id` from `file_sample`")
        file_hits=[]
        for item in files_json:
           file_hits.append(item['id'])
        print("file_hits inside current files")
        print(file_hits)
        return schema.Files(hits=file_hits)

    def get_current_cases(self):
        import schema

        cases_json=self.fetch_results("select id from participant")
        return schema.RepositoryCases(hits=[case['id'] for case in cases_json])

    def get_case(self,id):
        import schema

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

        print("inside get case")
        print(part_id)
        proj_json=self.fetch_results('''select distinct file_sample.project, project.id 
            from file_sample, project where file_sample.participant='''+str(part_id)+''' 
            and project.project_id=file_sample.project''')
        proj_id=proj_json[0]['id']
        print(proj_id)

        cat_raw_json=self.fetch_results(
            "select count(id) as raw_count from file_sample where participant="+str(part_id)+" and data_category='Raw Reads'")
        cat_raw_count=cat_raw_json[0]['raw_count']

        cat_taxa_json=self.fetch_results(
           "select count(id) as taxa_count from file_sample where participant="+str(part_id)+" and data_category='Taxonomic Profiles'")
        cat_taxa_count=cat_taxa_json[0]['taxa_count']

        cat_gene_json=self.fetch_results(
            "select count(id) as gene_count from file_sample where participant="+str(part_id)+" and data_category='Gene Families'")
        cat_gene_count=cat_gene_json[0]['gene_count']

        files_json=self.fetch_results("select * from file_sample where participant="+str(part_id))

        return schema.Case(id,
                    case_id="entity_participant_id",
                    primary_site="Stool",
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    project=self.get_project(proj_id),
                    summary=schema.Summary(
                      case_count=case_count,
                      file_count=file_count,
                      file_size=file_size,
                      data_categories=[schema.DataCategories(file_count=cat_raw_count, data_category="Raw Reads"),
                                       schema.DataCategories(file_count=cat_gene_count, data_category="Gene Families"),
                                       schema.DataCategories(file_count=cat_taxa_count, data_category="Taxonomic Profiles")]),
                      files=schema.CaseFiles(hits=[schema.CaseFile(
                               case_file['id'],
                               experimental_strategy=case_file['experimental_strategy'],
                               data_category=case_file['data_category'],
                               data_format=case_file['data_format'],
                               platform=case_file['platform'],
                               access=case_file['access']) for case_file in files_json]))


    def get_project_aggregations(self, projects):
        import schema

        # compile aggregations from project
        aggregates = {"primary_site": {}, "program__name": {},
                      "project_id": {}, 
                      "summary__data_categories__data_category": {},
                      "summary__experimental_strategies__experimental_strategy": {}}
        print("projects inside aggregations")

        for project in projects:
            print(
               project.id, project.project_id,project.summary.data_categories,project.primary_site,
               project.program,project.summary.experimental_strategies)
            add_key_increment(aggregates["primary_site"],project.primary_site[0])
            add_key_increment(aggregates["project_id"], project.project_id)
            add_key_increment(aggregates["program__name"], project.program[0])
            for item in project.summary.data_categories:
                add_key_increment(aggregates["summary__data_categories__data_category"], item)
            for item in project.summary.experimental_strategies:
                add_key_increment(aggregates["summary__experimental_strategies__experimental_strategy"], item)

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


    def get_current_counts(self):
        import schema

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
        import schema

        # aggregate file data
        aggregates = {"data_category": {}, "experimental_strategy": {},
                      "data_format": {}, "platform": {}, "cases__primary_site": {},
                      "cases__project__project_id": {}, "access": {}}

        for file in files:
            print(" values  inside file aggregation")
            print(file.data_category,file.experimental_strategy,file.data_format,file.platform,file.access)
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
        import schema

        # aggregate case data
        aggregates = {"demographic__ethnicity": {}, "demographic__gender": {},
                      "demographic__race": {}, "primary_site": {}, "project__project_id": {},
                      "project__program__name": {}}

        for case in cases:
            add_key_increment(aggregates["demographic__ethnicity"], case.demographic.ethnicity)
            add_key_increment(aggregates["demographic__gender"], case.demographic.gender)
            add_key_increment(aggregates["demographic__race"], case.demographic.race)
            add_key_increment(aggregates["primary_site"], case.primary_site)
            add_key_increment(aggregates["project__project_id"], case.project.project_id)
            add_key_increment(aggregates["project__program__name"], case.project.program.name)

        case_aggregates=schema.CaseAggregations(
            demographic__ethnicity=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__ethnicity"].items()]),
            demographic__gender=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__gender"].items()]),
            demographic__race=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__race"].items()]),
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__project_id"].items()]),
            project__program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__program__name"].items()]))

        return case_aggregates

    def get_facets(self):
        return "null" # this is not currently being used

    def get_cart_file_size(self):
        import schema

        file_json=self.fetch_results("select sum(file_size) as sum_size from  file_sample")
        return schema.FileSize(file_json[0]['sum_size'])

data = Data()
