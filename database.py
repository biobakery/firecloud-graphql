
# Calls to obtain values from the data structures (to be populated by the local database next)

import const

def add_key_increment(dictionary, key):
    if not key in dictionary:
        dictionary[key]=0
    dictionary[key]+=1

class Data(object):
    def load_data(self):
        self.data = const.DB()

    def get_total_projects_count(self):
        self.load_data()
        return len(self.data.CURRENT_PROJECTS.keys())

    def get_current_projects(self):
        self.load_data()
        return [self.get_project(project_id) for project_id in self.data.CURRENT_PROJECTS.keys()]

    def get_user(self):
        self.load_data()
        return self.data.CURRENT_USER

    def get_filecase(self,id):
        self.load_data()
        return self.data.CURRENT_FILE_CASES[id]

    def get_project(self,id):
        self.load_data()
        return self.data.CURRENT_PROJECTS[id]

    def get_file(self,id):
        self.load_data()
        return self.data.TEST_FILES[id]

    def get_total_files(self):
        self.load_data()
        return len(self.data.CURRENT_FILES.hits)

    def get_total_case_annotations(self):
        return 1 # not currently being used

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

    def get_project_aggregations(self):
        self.load_data()
        return self.data.PROJECT_AGGREGATIONS

    def get_current_counts(self):
        self.load_data()
        return self.data.CURRENT_COUNTS

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
            project = data.get_filecase(file.cases.hits[0]).project
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

    def get_case_aggregations(self):
        self.load_data()
        return self.data.CASE_AGGREGATIONS

    def get_total_cases_per_file(self):
        return 1 # this is currently not being used

    def get_total_cases(self):
        self.load_data()
        return len(self.data.TEST_CASES.keys())

    def get_facets(self):
        return "null" # this is not currently being used

    def get_cart_file_size(self):
        self.load_data()
        return self.data.CURRENT_FILE_SIZE

data = Data()
