# Calls to obtain values from the data structures (to be populated by the local database next)
import mysql.connector as mariadb
import os
import const

def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):

    db_conn = mariadb.connect(user='biom_mass', password=os.environ['BIOM_MASS'], db='portal_ui')

    # connects to db and runs query
    def fetch_results(self,query):

        cursor = self.db_conn.cursor(buffered=True)
        cursor.execute(query)

        # response
        row_headers=[x[0] for x in cursor.description]
        rows = cursor.fetchall()
        data=[]
        for row in rows:
            data.append(dict(zip(row_headers,row)))

        cursor.close()

        return data


    def load_data(self):
        self.data = const.DB()

    def get_current_projects(self):
        self.load_data()
        return [self.get_project(project_id) for project_id in self.data.CURRENT_PROJECTS.keys()]

    def get_user(self):
        self.load_data()
        return self.data.CURRENT_USER

    # get current version from db
    def get_current_version(self):
       import schema

       version_data=self.fetch_results("select * from version order by updated desc limit 1 ")
       del  version_data[0]['updated']
       del  version_data[0]['id']
       return schema.Version(**version_data[0])

    def get_project(self,id):
        self.load_data()
        return self.data.CURRENT_PROJECTS[id]

    def get_file(self,id):
        self.load_data()
        return self.data.TEST_FILES[id]

    def get_case_annotation(self):
        self.load_data()
        return self.data.CURRENT_CASE_ANNOTATION

    def get_current_files(self):
        self.load_data()
        return self.data.CURRENT_FILES

    def get_current_cases(self):
        self.load_data()
        return self.data.CURRENT_CASES

    def get_case(self,id):
        self.load_data()
        return self.data.TEST_CASES[id]

    def get_project_aggregations(self, projects):
        import schema

        self.load_data()

        # compile aggregations from project
        aggregates = {"primary_site": {}, "program__name": {},
                      "project_id": {}, 
                      "summary__data_categories__data_category": {},
                      "summary__experimental_strategies__experimental_strategy": {}}

        for project in projects:
            add_key_increment(aggregates["primary_site"], project.primary_site[0])
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
        import schema

        counts_data = self.fetch_results('''select count(id) as countid from project
                                            union all select count(id) as countid from participant
                                            union all select count(id) as countid from sample
                                            union all select count(distinct data_format) as countid from file_sample
                                            union all select count(id) as countid from file_sample where  type="rawFiles"
                                            union all select count(id) as countid from file_sample where type="processedFiles"''')

        return schema.Count(
                    projects=counts_data[0]['countid'],
                    participants=counts_data[1]['countid'],
                    samples=counts_data[2]['countid'],
                    dataFormats=counts_data[3]['countid'],
                    rawFiles=counts_data[4]['countid'],
                    processedFiles=counts_data[5]['countid'])


    def get_file_aggregations(self, files):
        import schema

        self.load_data()
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
        import schema

        self.load_data()

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
        self.load_data()
        return self.data.CURRENT_FILE_SIZE

data = Data()
