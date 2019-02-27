
# Calls to obtain values from the data structures (to be populated by the local database next)

import const

def get_data():
    return const.db()

def get_total_projects_count():
    return len(get_data().CURRENT_PROJECTS.keys())

def get_current_projects():
    return [get_project(project_id) for project_id in get_data().CURRENT_PROJECTS.keys()]

def get_user():
    return get_data().CURRENT_USER

def get_filecase(id):
    return get_data().CURRENT_FILE_CASES[id]

def get_project(id):
    return get_data().CURRENT_PROJECTS[id]

def get_file(id):
    return get_data().TEST_FILES[id]

def get_total_files():
    return len(get_data().CURRENT_FILES.hits)

def get_total_case_annotations():
    return 1 # not currently being used

def get_case_annotation():
    return get_data().CURRENT_CASE_ANNOTATION

def get_current_files():
    return get_data().CURRENT_FILES

def get_current_cases():
    return get_data().CURRENT_CASES

def get_case(id):
    return get_data().TEST_CASES[id]

def get_project_aggregations():
    return get_data().PROJECT_AGGREGATIONS

def get_current_counts():
    return get_data().CURRENT_COUNTS

def get_file_aggregations():
    return get_data().FILE_AGGREGATIONS

def get_case_aggregations():
    return get_data().CASE_AGGREGATIONS

def get_total_cases_per_file():
    return 1 # this is currently not being used

def get_total_cases():
    return len(get_data().TEST_CASES.keys())

def get_facets():
    return "null" # this is not currently being used

def get_cart_file_size():
    return get_data().CURRENT_FILE_SIZE


