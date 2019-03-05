
# Calls to obtain values from the data structures (to be populated by the local database next)

import const

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

    def get_file_aggregations(self):
        self.load_data()
        return self.data.FILE_AGGREGATIONS

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

