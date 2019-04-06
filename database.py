
# Calls to obtain values from the data structures, populated by the local cache database

import sqlalchemy
import sys

import utilities
import schema

RAW_FILE_TYPE = "rawFiles"
PROCESSED_FILE_TYPE = "processedFiles"

class Data(object):

    def __init__(self):
        # get the database environment variables
        username, password, database = utilities.get_database_variables()

        # create a pool of connections, recycle so they do not become stale
        database_url = "mysql://{username}:{password}@localhost/{database}".format(username = username,
            password = password, database = database)

        try:
            self.engine = sqlalchemy.create_engine(database_url, pool_size=32, pool_recycle=3600)
        except EnvironmentError as e:
            print("Unable to connect to local database")
            print("Database url {}".format(database_url))
            sys.exit(e)

    def query_database(self, query, fetchall=False):
        # obtain connection from pool, run query
        # then release connection back to pool
        connection = self.engine.connect()
        results = connection.execute(query)
  
        # if fetchall then get all results (to close cursor)
        # and then close connection
        # if not, then return connction so function can
        # iterate on results and then close connection
        if fetchall:
            results = results.fetchall()
            connection.close()
            return results
        else:
            return connection, results

    def get_current_projects(self):
        query = "SELECT file_sample.id as file_id, file_sample.participant, " +\
                 "file_sample.file_size, file_sample.data_category, " +\
                 "file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "participant.id as participant_id, project.program " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id " +\
                 "INNER JOIN participant ON file_sample.participant=participant.entity_participant_id"
        connection, db_results = self.query_database(query)
        project_info = {}
        for row in db_results:
            id = row['project_id']
            if not id in project_info:
                project_info[id]={"file_size":0, "file_count":0, "participants":set(), "data_category": {}, "experimental_strategy": {}}
                project_info[id]['name']=row['project']
                project_info[id]['program']=row['program']
                project_info[id]['primary_site']=row['primary_site']
            # compile file size
            project_info[id]['file_size']+=int(row['file_size'])
            # compile file count
            project_info[id]['file_count']+=1
            # compile cases
            project_info[id]['participants'].add(row['participant_id'])
            # count data category and experimental strategy
            for count_type in ["data_category", "experimental_strategy"]:
                project_info[id][count_type][row[count_type]]=project_info[id][count_type].get(row[count_type],0)+1

        connection.close()
        projects = []
        for id, info in project_info.items():
            projects.append(schema.Project(
                id=id,
                project_id=info['name'],
                name=info['name'],
                program=schema.Program(name=info['program']),
                summary=schema.Summary(case_count=len(list(info['participants'])),
                    file_count=info['file_count'],
                    data_categories=[schema.DataCategories(case_count=value, data_category=key) for key,value in info['data_category'].items()],
                    experimental_strategies=[schema.ExperimentalStrategies(file_count=value, experimental_strategy=key) for key,value in info['experimental_strategy'].items()],
                    file_size=info['file_size']),
                primary_site=[info['primary_site']]))

        return projects

    def get_current_files(self):
        query = "SELECT file_sample.id as file_id, file_sample.file_name, file_sample.participant, file_sample.sample, " +\
                 "file_sample.access, file_sample.file_size, file_sample.data_category, file_sample.data_format, " +\
                 "file_sample.platform, file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "participant.id as participant_id, project.program, " +\
                 "participant.age_2012 as age, participant.weight_lbs as weight, participant.totMETs1 as met " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id " +\
                 "INNER JOIN participant ON file_sample.participant=participant.entity_participant_id"
        connection, db_results = self.query_database(query)
        files = []
        for row in db_results:
            files.append(schema.File(
                id=row['file_id'],
                name=row['file_name'],
                participant=row['participant'],
                sample=row['sample'],
                access=row['access'],
                file_size=row['file_size'],
                data_category=row['data_category'],
                data_format=row['data_format'],
                platform=row['platform'],
                experimental_strategy=row['experimental_strategy'],
                file_name=row['file_name'],
                cases=schema.FileCases(
                    hits=[schema.FileCase(
                        id=row['participant_id'],
                        case_id=row['participant'],
                        project=schema.Project(
                            id=row['project_id'],
                            project_id=row['project'],
                            name=row['project'],
                            program=schema.Program(name=row['program']),
                            primary_site=[row['primary_site']]),
                        demographic=schema.Demographic(
                            age=row['age'],
                            weight=row['weight'],
                            met=row['met']), 
                        primary_site=row['primary_site'])]
                ),
                file_id=row['file_id'],
                type=row['data_format']
            ))
        connection.close()
        return files

    def get_current_cases(self):
        # gather file data for participants
        query = "SELECT id, participant, file_size, data_category, experimental_strategy, " +\
                "data_format, platform, access from file_sample"
        connection, db_results = self.query_database(query)
        case_files = {}
        for row in db_results:
            if not row['participant'] in case_files:
                case_files[row['participant']] = []
            case_files[row['participant']].append(dict(row.items()))
        connection.close()

        # gather participant data
        query = "SELECT participant.id as participant_id, participant.entity_participant_id as participant_name, project.primary_site as primary_site, " +\
                 "project.id as project_id, project.project_id as project_name, project.program as program_name, " +\
                 "participant.age_2012 as age, participant.weight_lbs as weight, participant.totMETs1 as met " +\
                 "FROM sample INNER JOIN participant ON sample.participant=participant.entity_participant_id " +\
                 "INNER JOIN project ON sample.project=project.project_id"
        connection, db_results = self.query_database(query)
        cases = []
        completed_cases = set()
        for row in db_results:
            if row['participant_id'] in completed_cases:
                continue
            current_case_files = case_files[row['participant_name']]
            # create data categories
            data_categories_counts={}
            for case_row in current_case_files:
                data_categories_counts[case_row['data_category']]=data_categories_counts.get(case_row['data_category'],0)+1
            data_categories = [schema.DataCategories(case_count=value, data_category=key) for key, value in data_categories_counts.items()]
 
            # create participant summary
            summary=schema.Summary(case_count=1, 
                                   file_count=len(current_case_files),
                                   file_size=sum(map(int, [case_row['file_size'] for case_row in current_case_files])),
                                   data_categories=data_categories)

            # create participant casefiles
            casefiles=[]
            for index, file_info in enumerate(current_case_files):
                casefiles.append(schema.CaseFile(
                    id=index,
                    data_category=file_info['data_category'],
                    experimental_strategy=file_info['experimental_strategy'],
                    data_format=file_info['data_format'],
                    platform=file_info['platform'],
                    access=file_info['access']))

            cases.append(schema.Case(
                id=row['participant_id'],
                case_id=row['participant_name'],
                primary_site=row['primary_site'],
                demographic=schema.Demographic(
                    age=row['age'],
                    weight=row['weight'],
                    met=row['met']),
                project=schema.Project(
                    id=row['project_id'],
                    project_id=row['project_name'],
                    name=row['project_name'],
                    program=schema.Program(name=row['program_name']),
                    primary_site=[row['primary_site']]),
                summary=summary,
                files=schema.CaseFiles(hits=casefiles)
            ))
            completed_cases.add(row['participant_id'])
        connection.close()
        return cases

    def get_cart_file_size(self):
        db_results = self.query_database("SELECT SUM(file_size) from file_sample", fetchall=True)[0][0]
        return schema.FileSize(db_results)

    def get_current_counts(self):
        query = "SELECT COUNT(distinct project), COUNT(distinct participant), COUNT(distinct sample), " +\
                "COUNT(distinct data_format), COUNT(IF(type='"+RAW_FILE_TYPE+"',1,NULL)), " +\
                "COUNT(IF(type='"+PROCESSED_FILE_TYPE+"',1,NULL)) FROM file_sample"
        db_results = self.query_database(query, fetchall=True)[0]
        counts = schema.Count(
            projects=db_results[0],
            participants=db_results[1],
            samples=db_results[2],
            dataFormats=db_results[3],
            rawFiles=db_results[4], 
            processedFiles=db_results[5]
        )
        return counts

    def get_version(self):
        db_results = self.query_database("SELECT commit, data_release, status, tag, version FROM version", fetchall=True)[0]
        return dict(db_results.items())

    #############################################################################
    ## Aggregations section
    ## These functions create aggregations of the object lists they are provided.
    #############################################################################

    def get_project_aggregations(self, projects):
        # compile aggregations from project
        aggregates = {"primary_site": {}, "program__name": {},
                      "project_id": {}, 
                      "summary__data_categories__data_category": {},
                      "summary__experimental_strategies__experimental_strategy": {}}

        for project in projects:
            utilities.add_key_increment(aggregates["primary_site"], project.primary_site[0])
            utilities.add_key_increment(aggregates["project_id"], project.project_id)
            utilities.add_key_increment(aggregates["program__name"], project.program.name)
            for item in project.summary.data_categories:
                utilities.add_key_increment(aggregates["summary__data_categories__data_category"], item.data_category)
            for item in project.summary.experimental_strategies:
                utilities.add_key_increment(aggregates["summary__experimental_strategies__experimental_strategy"], item.experimental_strategy)

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

    def get_file_aggregations(self, files):
        # aggregate file data
        aggregates = {"data_category": {}, "experimental_strategy": {},
                      "data_format": {}, "platform": {}, "cases__primary_site": {},
                      "cases__project__project_id": {}, "access": {}}

        for file in files:
            utilities.add_key_increment(aggregates["data_category"], file.data_category)
            utilities.add_key_increment(aggregates["experimental_strategy"], file.experimental_strategy)
            utilities.add_key_increment(aggregates["data_format"], file.data_format)
            utilities.add_key_increment(aggregates["platform"], file.platform)
            utilities.add_key_increment(aggregates["access"], file.access)
            project = file.cases.hits[0].project
            utilities.add_key_increment(aggregates["cases__primary_site"], project.primary_site[0])
            utilities.add_key_increment(aggregates["cases__project__project_id"], project.project_id)

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
        aggregates = {"primary_site": {}, "project__project_id": {},
                      "project__program__name": {}, "demographic__age": {}, "demographic__weight": {}, "demographic__met": {} }

        for case in cases:
            utilities.add_key_increment(aggregates["demographic__age"], case.demographic.age)
            utilities.add_key_increment(aggregates["demographic__weight"], case.demographic.weight)
            utilities.add_key_increment(aggregates["demographic__met"], case.demographic.met)
            utilities.add_key_increment(aggregates["primary_site"], case.primary_site)
            utilities.add_key_increment(aggregates["project__project_id"], case.project.project_id)
            utilities.add_key_increment(aggregates["project__program__name"], case.project.program.name)

        case_aggregates=schema.CaseAggregations(
            demographic__age=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__age"].items()]),
            demographic__weight=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__weight"].items()]),
            demographic__met=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__met"].items()]),
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__project_id"].items()]),
            project__program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__program__name"].items()]))

        return case_aggregates

    #############################################################################
    ## Default constant section
    ## These functions return default constants are they are not currently in use.
    ## They will be placed in use in later versions of the server.
    #############################################################################

    def get_user(self):
        return schema.User(username="null") # no users currently set
    
    def get_case_annotation(self):
        return schema.CaseAnnotation() # not currently used

    def get_facets(self):
        return "null" # this is not currently being used

data = Data()
