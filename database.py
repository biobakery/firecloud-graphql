
# Calls to obtain values from the data structures, populated by the local cache database

import sqlalchemy
import sys
import time
import threading

import utilities
import schema

RAW_FILE_TYPE = "rawFiles"
PROCESSED_FILE_TYPE = "processedFiles"
GENERIC_FILE_NAME_OFFSET = 1000000

CASE_DEFAULT_COLUMNS = set(['entity_participant_id', 'updated', 'participant_name', 'participant_id', 'id'])
SAMPLE_DEFAULT_COLUMNS = set(['sample', 'updated', 'participant', 'sample_id', 'id','project'])

# metadata keys to move to the front of the list to show on the site (in aggregations and as first in the tables)
METADATA_DEMOGRAPHICS_PROMOTE=["project","state","age","weight","race","ethnicity","diagnosis","alcohol","caffiene","smoking"]
METADATA_SAMPLES_PROMOTE=["time","week","fiber","fat","b12","carbs","protein","folate","calories","iron"]

# optional white list of metadata keys to use
METADATA_DEMOGRAPHICS_WHITELIST="demographic_metadata_whitelist.txt"
METADATA_SAMPLES_WHITELIST="sample_metadata_whitelist.txt"

class Cache(object):

    def __init__(self):
        self.expires={}
        # expires every 3 months
        self.expires_offset=60*60*24*30*3

        self.lock=threading.Lock()

        self.cache={}

    def get_cache(self,cache_type,filters):
        self.lock.acquire()

        cache_name=cache_type+filters

        #if ( self.expires.get(cache_name,0) + self.expires_offset ) > time.time() and cache_name in self.cache:
        if cache_name in self.cache:
            value = self.cache[cache_name]
            self.lock.release()
            have_lock=False
        else:
            have_lock=True
            value = ""

        return value, have_lock

    def update_cache(self,cache_type,new_object,filters,have_lock):
        if not have_lock:
            self.lock.acquire()

        cache_name=cache_type+filters

        self.cache[cache_name]=new_object
        self.expires[cache_name]=time.time()

        self.lock.release()

# all data objects share the same cache
cache = Cache()

class Data(object):

    def __init__(self):
        # get the database environment variables
        username, password, database = utilities.get_database_variables()

        # set defaults for metadata names
        self.sample_metadata_columns=[]
        self.participant_metadata_columns=[]

        # create a pool of connections, pre-ping to prevent stale connections
        database_url = "mysql://{username}:{password}@localhost/{database}".format(username = username,
            password = password, database = database)

        try:
            self.engine = sqlalchemy.create_engine(database_url, pool_size=32, pool_pre_ping=True)
        except EnvironmentError as e:
            print("Unable to connect to local database")
            print("Database url {}".format(database_url))
            sys.exit(e)

        self.cache=cache

        # set the no access group
        self.no_access_group = "'None'"

        # check for optional whitelist files
        self.metadata_demographics_whitelist=utilities.read_whitelist(METADATA_DEMOGRAPHICS_WHITELIST)
        self.metadata_samples_whitelist=utilities.read_whitelist(METADATA_SAMPLES_WHITELIST)


    def query_database(self, query, fetchall=False, no_results=False):
        # obtain connection from pool, run query
        # then release connection back to pool
        
        connection = self.engine.connect()
        if no_results:
            connection.execute(query)
            connection.close()
            return None
        else:
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

    def add_token(self, email, token):
        # add or update the token for the user to 48 hours from now plus 5 min (to allow for UI time diff from server)
        expires = time.time()+2*24*60*60+5*60
        db_results = self.query_database("UPDATE users SET token='{0}', expires='{1}' WHERE email='{2}'".format(token,expires,email), no_results=True)

    def create_access_query_restriction(self, projects):
        return " WHERE project in ({}) ".format(projects)

    def set_project_access_filters(self, projects):
        self.project_access_filters=self.create_access_query_restriction(projects)
        if projects == self.no_access_group:
            self.project_access = False
        else:
            self.project_access = True

    def get_project_access_filters(self):
        return self.project_access_filters

    def valid_token(self, token):
        access_groups = self.get_project_access(token)
        if access_groups == self.no_access_group:
            return False
        else:
            return True

    def get_project_access(self, token):
        db_results = self.query_database("SELECT email, expires, projects FROM users WHERE token='{}'".format(token), fetchall=True)
        if db_results:
            # check if the token has expired
            current_time = time.time()
            try:
                expires = float(db_results[0][1])
            except ValueError:
                expires = current_time
          
            if current_time > expires:
                db_results = self.query_database("UPDATE users SET token='{0}', expires='{1}' WHERE email='{2}'".format("None","None",db_results[0][0]), no_results=True)
                return self.no_access_group
            elif current_time < expires:
                return db_results[0][2]
            else:
                return self.no_access_group
        else:
            return self.no_access_group

    def valid_user(self, email):
        db_results = self.query_database("SELECT token FROM users WHERE email='{}'".format(email), fetchall=True)
        if db_results:
            return True
        else:
            return False

    def get_current_projects(self, filters=None):
        query = "SELECT file_sample.id as file_id, file_sample.participant, " +\
                 "file_sample.file_size, file_sample.data_category, " +\
                 "file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "participant.id as participant_id, project.program " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id " +\
                 "INNER JOIN participant ON file_sample.participant=participant.entity_participant_id"
        connection, db_results = self.query_database(query)

        # create a set of files for filtering
        save_db_results=[]
        all_files=[]
        saved_files=set()
        for row in db_results:
            all_files.append(schema.File(id=row['file_id'], data_category=row['data_category'], experimental_strategy=row['experimental_strategy']))
            save_db_results.append(row)
            saved_files.add(row['file_id'])

        query = "SELECT file_sample.id as file_id, file_sample.participant, " +\
                 "file_sample.file_size, file_sample.data_category, " +\
                 "file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "project.program, project.total_participants " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id "
        connection, db_results = self.query_database(query)

        # create a set of files for filtering
        for row in db_results:
            if not row['file_id'] in saved_files:
                all_files.append(schema.File(id=row['file_id'], data_category=row['data_category'], experimental_strategy=row['experimental_strategy']))
                save_db_results.append(row)
                saved_files.add(row['file_id'])

        # apply filtering only for summary/file filters
        if filters and "content" in filters:
            for content in filters["content"]:
                field=content["content"]["field"]
                if "summary" in field:
                    content["content"]["field"]="files."+field.split(".")[-1]
            filtered_files = utilities.filter_hits(all_files, filters, "files", True)
            selected_file_ids = [file.id for file in filtered_files]
        else:
            selected_file_ids = [file.id for file in all_files]

        project_info = {}
        for row in save_db_results:
            id = row['project_id']
            if not row['file_id'] in selected_file_ids:
                continue
            if not id in project_info:
                project_info[id]={"file_size":0, "file_count":0, "participants":set(), "data_category": {}, "experimental_strategy": {}}
                project_info[id]['name']=row['project']
                project_info[id]['program']=row['program']
                project_info[id]['primary_site']=row['primary_site']
            # compile file size
            project_info[id]['file_size']+=int(row['file_size'])
            # compile cases
            if "participant_id" in row:
                project_info[id]['participants'].add(row['participant_id'])
            # add NA participants for counts only for projects without participant metadata
            elif "total_participants" in row and row['total_participants']:
                project_info[id]['participants'].update(map(lambda x: "NA_"+row['project']+"_"+str(x), list(xrange(int(row['total_participants'])))))
            # compile file count and count data category and experimental strategy
            if row['file_size'] != "0":
                project_info[id]['file_count']+=1
            
                for count_type in ["data_category", "experimental_strategy"]:
                    project_info[id][count_type][row[count_type]]=project_info[id][count_type].get(row[count_type],0)+1

        connection.close()

        query = "SELECT sample.id as sample_id, sample.participant as participant_id, sample.project, " +\
                 "project.id as project_id, project.primary_site, " +\
                 "project.program " +\
                 "FROM sample INNER JOIN project ON sample.project=project.project_id"
        connection, db_results = self.query_database(query)

        for row in db_results:
            id = row['project_id']
            if not id in project_info:
                project_info[id]={"file_size":0, "file_count":0, "participants":set(), "data_category": {}, "experimental_strategy": {}}
                project_info[id]['name']=row['project']
                project_info[id]['program']=row['program']
                project_info[id]['primary_site']=row['primary_site']
            # compile cases
            project_info[id]['participants'].add(row['participant_id'])

        connection.close()

        query = "SELECT project_id, total_participants FROM project"
        connection, db_results = self.query_database(query)
        total_participants={}
        for row in db_results:
            total_participants[row['project_id']]=int(row['total_participants'])

        connection.close()


        projects = []
        for id, info in project_info.items():
            projects.append(schema.Project(
                id=id,
                project_id=info['name'],
                name=info['name'],
                program=schema.Program(name=info['program']),
                summary=schema.Summary(case_count=total_participants.get(info['name'],0),
                    file_count=info['file_count'],
                    data_categories=[schema.DataCategories(case_count=value, data_category=key) for key,value in info['data_category'].items()],
                    experimental_strategies=[schema.ExperimentalStrategies(file_count=value, experimental_strategy=key) for key,value in info['experimental_strategy'].items()],
                    file_size=info['file_size']),
                primary_site=[info['primary_site']]))

        return projects

    @staticmethod
    def get_generic_file_name(file_id, extension):
        return "{0}.{1}".format(int(file_id)+GENERIC_FILE_NAME_OFFSET, extension.lower())

    def get_all_cases(self,rows=False,filters=""):
        query = "SELECT participant.* from participant INNER JOIN sample ON participant.entity_participant_id = sample.participant "+filters;
        connection, db_results_participant = self.query_database(query)

        # organize based on participant id
        participant_data = {}
        for rowprox in db_results_participant:
            row = dict(rowprox.items())
            row['participant_id']=row['id']
            row['participant_name']=row['entity_participant_id']

            participant_data[row['entity_participant_id']]=row
        
        metadata_columns=[]
        if rows:
            participant_data = participant_data.values()
            try:
                metadata_columns = list(set(participant_data[0].keys()).difference(CASE_DEFAULT_COLUMNS))
            except IndexError:
                metadata_columns=[]
        else:
            try:
                metadata_columns = list(set(participant_data[participant_data.keys()[0]].keys()).difference(CASE_DEFAULT_COLUMNS))
            except IndexError:
                metadata_columns=[]

        if metadata_columns and participant_data:
            self.participant_metadata_columns=metadata_columns

        return metadata_columns, participant_data

    def get_all_samples(self,rows=False,filters=""):
        query = "SELECT * from sample "+filters;
        connection, db_results_sample = self.query_database(query)

        # organize based on sample id
        sample_data = {}
        for rowprox in db_results_sample:
            row = dict(rowprox.items())
            # add custom name changes
            row['sample_id']=row['id']

            sample_data[row['sample']]=row

        if rows:
            sample_data=sample_data.values()
            try:
                metadata_columns = list(set(sample_data[0].keys()).difference(SAMPLE_DEFAULT_COLUMNS))
            except IndexError:
                metadata_columns=[]
        else:
            try:
                metadata_columns = list(set(sample_data[sample_data.keys()[0]].keys()).difference(SAMPLE_DEFAULT_COLUMNS))
            except IndexError:
                metadata_columns=[]

        if metadata_columns and sample_data:
            self.sample_metadata_columns=metadata_columns

        return metadata_columns, sample_data 

    def get_all_projects(self):
        query = "SELECT * FROM project"
        connection, db_results = self.query_database(query)

        projects_results={}
        for rowprox in db_results:
            row = dict(rowprox.items())
            row['project_name']=row['project_id']
            row['project_id']=row['id']
            row['program_name']=row['program']

            projects_results[row['project_name']]=row

        return projects_results

    def get_current_files(self, filters=""):
       
        cache_files, have_lock=self.cache.get_cache("files",filters)
        if cache_files:
            return cache_files

        # get all cases and samples data
        participant_metadata_columns, participant_data = self.get_all_cases(filters=filters)
        sample_metadata_columns, sample_data = self.get_all_samples(filters=filters)

        query = "SELECT file_sample.id as file_id, file_sample.file_id as file_url, file_sample.file_name as file_name, file_sample.participant, file_sample.sample, " +\
                 "file_sample.access, file_sample.file_size, file_sample.data_category, file_sample.data_format, " +\
                 "file_sample.platform, file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "project.program " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id WHERE file_sample.file_id !='NA'"

        connection, db_results = self.query_database(query)
        files = []
        for row in db_results:
            # add in the sample and participant data
            db_case=participant_data.get(row['participant'],{})
            db_sample=sample_data.get(row['sample'],{})

            metadataCase_hits=[]
            if db_case:
                for demo_item in participant_metadata_columns:
                    metadataCase_hits.append(schema.MetadataCaseAnnotation(id=str(db_case['participant_id'])+demo_item,metadataKey=demo_item[0].upper()+demo_item[1:],metadataValue=db_case[demo_item]))
            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA' and x.metadataValue != "Not_available", metadataCase_hits)))

            demographic_instance=None
            if db_case:
                demographic_instance=schema.Custom()
                demographic_keys=participant_metadata_columns
                schema.add_attributes(demographic_instance, demographic_keys, db_case)

            casesample_instance=None
            if db_sample:
                casesample_instance=schema.CaseSample(id=db_sample.get('sample_id',1))
                casesample_keys=sample_metadata_columns
                schema.add_attributes(casesample_instance, casesample_keys, db_sample)

            files.append(schema.File(
                id=row['file_id'],
                file_url=row['file_url'],
                participant=row['participant'],
                sample=row['sample'],
                access=row['access'],
                file_size=row['file_size'],
                data_category=row['data_category'],
                data_format=row['data_format'],
                platform=row['platform'],
                experimental_strategy=row['experimental_strategy'],
                generic_file_name=row['file_name'],
                cases=schema.FileCases(
                    hits=[schema.FileCase(
                        id=row['participant'],
                        case_id=row['participant'],
                        project=schema.Project(
                            id=row['project_id'],
                            project_id=row['project'],
                            name=row['project'],
                            program=schema.Program(name=row['program']),
                            primary_site=[row['primary_site']]),
                        demographic=demographic_instance,
                        metadataCase=schema.MetadataCase(
                            hits=metadataCase_hits,
                            metadata_count=metadataCase_counts),
                        primary_site=row['primary_site'],
                        samples=[casesample_instance] if casesample_instance else []
                        )]
                ),
                file_id=row['file_id'],
                type=row['data_format']
            ))
        connection.close()

        self.cache.update_cache("files",files,filters,have_lock)

        return files

    def get_current_samples(self,filters=""):

        cache_samples, have_lock = self.cache.get_cache("samples", filters)
        if cache_samples:
            return cache_samples

        # gather file data for participants
        query = "SELECT id, participant, file_size, data_category, experimental_strategy, " +\
                "data_format, platform, access, project from file_sample WHERE file_id !='NA'"
        connection, db_results = self.query_database(query)
        case_files = {}
        merged_case_files = {}
        for row in db_results:
            if row['participant'] == "NA":
                if not row['project'] in merged_case_files:
                    merged_case_files[row['project']] = []
                merged_case_files[row['project']].append(dict(row.items()))

            if not row['participant'] in case_files:
                case_files[row['participant']] = []
            case_files[row['participant']].append(dict(row.items()))
        connection.close()

        # get all cases and samples data
        participant_metadata_columns, participant_data = self.get_all_cases(filters=filters)
        projects_data = self.get_all_projects()
        sample_metadata_columns, db_results = self.get_all_samples(rows=True,filters=filters)

        samples = []
        for row in db_results:
            db_case = participant_data.get(row['participant'],False)
            db_projects = projects_data.get(row['project'],False)
            
            if not ( db_case and db_projects):
                continue

            current_case_files = case_files.get(row['participant'],[])

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
            all_case_files=merged_case_files.get(row['project'],[])+current_case_files
            for index, file_info in enumerate(all_case_files):
                casefiles.append(schema.CaseFile(
                    id=index,
                    data_category=file_info['data_category'],
                    experimental_strategy=file_info['experimental_strategy'],
                    data_format=file_info['data_format'],
                    platform=file_info['platform'],
                    access=file_info['access'],
                    file_size=file_info['file_size']))

            metadataCase_hits=[]
            for demo_item in participant_metadata_columns:
                schema.MetadataCaseAnnotation(id=str(db_case['participant_id'])+demo_item,metadataKey=demo_item[0].upper()+demo_item[1:],metadataValue=db_case[demo_item]),

            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA' and x.metadataValue != "Not_available", metadataCase_hits)))

            metadataSample_hits=[]
            for metadata_key in sample_metadata_columns:
                metadataSample_hits.append(schema.MetadataSampleAnnotation(id=str(row['id'])+metadata_key,metadataKey=metadata_key.title(),metadataValue=row[metadata_key]))

            metadataSample_counts=len(list(filter(lambda x: x.metadataValue != 'NA' and x.metadataValue != "Not_available", metadataSample_hits)))

            demographic_instance=schema.Custom()
            demographic_keys=participant_metadata_columns
            schema.add_attributes(demographic_instance, demographic_keys,db_case)

            sample_instance=schema.Sample(
                id=row['id'],
                sample_id=row['sample'],
                primary_site=db_projects['primary_site'],
                demographic=demographic_instance,
                metadataCase=schema.MetadataCase(
                    hits=metadataCase_hits,
                    metadata_count=metadataCase_counts),
                project=schema.Project(
                    id=db_projects['project_id'],
                    project_id=db_projects['project_name'],
                    name=db_projects['project_name'],
                    program=schema.Program(name=db_projects['program_name']),
                    primary_site=[db_projects['primary_site']]),
                summary=summary,
                metadataSample=schema.MetadataSample(
                    hits=metadataSample_hits,
                    metadata_count=metadataSample_counts),
                files=schema.CaseFiles(hits=casefiles),
                cases=schema.FileCases(hits=[schema.FileCase(case_id=db_case['participant_id'], primary_site=db_projects['primary_site'])])
            )

            sample_keys=sample_metadata_columns
            schema.add_attributes(sample_instance, sample_keys, row)

            samples.append(sample_instance)
        connection.close()

        self.cache.update_cache("samples",samples,filters,have_lock)

        return samples


    def get_current_cases(self,filters=""):

        cache_cases, have_lock = self.cache.get_cache("cases", filters)
        if cache_cases:
            return cache_cases

        # gather file data for participants
        query = "SELECT id, participant, file_size, data_category, experimental_strategy, " +\
                "data_format, platform, access, project from file_sample WHERE file_id != 'NA'"
        connection, db_results = self.query_database(query)
        case_files = {}
        merged_case_files = {}
        for row in db_results:
            if row['participant'] == "NA":
                if not row['project'] in merged_case_files:
                    merged_case_files[row['project']] = []
                merged_case_files[row['project']].append(dict(row.items()))

            if not row['participant'] in case_files:
                case_files[row['participant']] = []
            case_files[row['participant']].append(dict(row.items()))

        connection.close()

        # gather sample data for participants
        sample_metadata_columns, db_results = self.get_all_samples(rows=True,filters=filters)
        case_samples = {}
        for row in db_results:
            if not row['participant'] in case_samples:
                case_samples[row['participant']] = []
            case_samples[row['participant']].append(dict(row.items()))
        connection.close()
        
        # gather participant data
        projects_data=self.get_all_projects()
        participant_metadata_columns, db_results=self.get_all_cases(rows=True,filters=filters)

        cases = []
        completed_cases = set()
        for row in db_results:
            db_sample=case_samples.get(row['participant_name'],[""])[0]

            if not db_sample:
                continue

            db_projects=projects_data.get(db_sample['project'],False)

            if not db_projects:
                continue

            if row['participant_id'] in completed_cases:
                continue

            current_case_files = case_files.get(row['participant_name'],[])
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
            all_case_files=merged_case_files.get(db_sample['project'],[])+current_case_files
            for index, file_info in enumerate(all_case_files):
                casefiles.append(schema.CaseFile(
                    id=index,
                    data_category=file_info['data_category'],
                    experimental_strategy=file_info['experimental_strategy'],
                    data_format=file_info['data_format'],
                    platform=file_info['platform'],
                    access=file_info['access'],
                    file_size=file_info['file_size']))

            # create casesamples
            casesamples=[]
            for index, sample_info in enumerate(case_samples[row['participant_name']]):
                casesample_instance=schema.CaseSample(id=index)

                casesample_keys=sample_metadata_columns
                schema.add_attributes(casesample_instance, casesample_keys, sample_info)
                
                casesamples.append(casesample_instance)

            metadataCase_hits=[]
            for demo_item in participant_metadata_columns:
                metadataCase_hits.append(schema.MetadataCaseAnnotation(id=str(row['participant_id'])+demo_item,metadataKey=demo_item[0].upper()+demo_item[1:],metadataValue=row[demo_item]))

            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA', metadataCase_hits)))

            demographic_instance=schema.Custom()
            demographic_keys=participant_metadata_columns
            schema.add_attributes(demographic_instance, demographic_keys, row)

            cases.append(schema.Case(
                id=row['participant_id'],
                case_id=row['participant_name'],
                primary_site=db_projects['primary_site'],
                demographic=demographic_instance,
                metadataCase=schema.MetadataCase(
                    hits=metadataCase_hits,
                    metadata_count=metadataCase_counts),
                project=schema.Project(
                    id=db_projects['project_id'],
                    project_id=db_projects['project_name'],
                    name=db_projects['project_name'],
                    program=schema.Program(name=db_projects['program_name']),
                    primary_site=[db_projects['primary_site']]),
                summary=summary,
                files=schema.CaseFiles(hits=casefiles),
                samples=schema.CaseSamples(hits=casesamples),
            ))
            completed_cases.add(row['participant_id'])
        connection.close()

        self.cache.update_cache("cases",cases,filters,have_lock)

        return cases

    def get_cart_file_size(self, filters=""):
        all_files = self.get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files", True)
        # get the size from the filtered files
        total_size = sum([utilities.str_to_float([file.file_size], error_zero=True)[0] for file in filtered_files])
        return schema.CartSummaryAggs(fs=schema.FileSize(value=total_size))

    def get_current_counts(self):
        query = "SELECT COUNT(distinct project), COUNT(distinct participant), COUNT(distinct sample), " +\
                "COUNT(distinct IF(data_format!='NA',1,data_format)), COUNT(IF(type='"+RAW_FILE_TYPE+"',1,NULL)), " +\
                "COUNT(IF(type='"+PROCESSED_FILE_TYPE+"',1,NULL)) FROM file_sample"
        db_results = self.query_database(query, fetchall=True)[0]

        query = "SELECT SUM(total_participants) FROM project"
        db_results_2 = self.query_database(query, fetchall=True)[0]

        # the count for data_format above does not sync up so using this alternative
        query = "SELECT COUNT(distinct data_format) FROM file_sample where data_format!='NA'"
        db_results_3 = self.query_database(query, fetchall=True)[0]

        counts = schema.Count(
            projects=db_results[0],
            participants=int(db_results_2[0]),
            samples=db_results[2],
            dataFormats=int(db_results_3[0]),
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
        def get_schema_aggregations(variable_name,schema_type="buckets"):
            if schema_type == "buckets":
                return schema.Aggregations(
                    buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[variable_name].items()])
            else:
                return schema.Aggregations(
                    stats=schema.Stats(max=stats[variable_name].get("max",0), min=stats[variable_name].get("min",0)))

        # aggregate file data
        aggregates = {"data_category": {}, "experimental_strategy": {},
                      "data_format": {}, "platform": {}, "cases__primary_site": {},
                      "cases__project__project_id": {}, "access": {}, "file_size": {}}
        stats = {"file_size": {}}

        for file in files:
            utilities.add_key_increment(aggregates["data_category"], file.data_category)
            utilities.add_key_increment(aggregates["experimental_strategy"], file.experimental_strategy)
            utilities.add_key_increment(aggregates["data_format"], file.data_format)
            utilities.add_key_increment(aggregates["platform"], file.platform)
            utilities.add_key_increment(aggregates["access"], file.access)
            utilities.add_key_increment(aggregates["file_size"], utilities.Range.create_custom(utilities.bytes_to_gb(file.file_size),2))
            try:
                project = file.cases.hits[0].project
                utilities.add_key_increment(aggregates["cases__primary_site"], project.primary_site[0])
                utilities.add_key_increment(aggregates["cases__project__project_id"], project.project_id)
            except IndexError:
                continue

            utilities.update_max_min(stats["file_size"], utilities.bytes_to_gb(file.file_size))


        file_aggregates = schema.FileAggregations(
            data_category=get_schema_aggregations("data_category"),
            experimental_strategy=get_schema_aggregations("experimental_strategy"),
            data_format=get_schema_aggregations("data_format"),
            platform=get_schema_aggregations("platform"),
            cases__primary_site=get_schema_aggregations("cases__primary_site"),
            access=get_schema_aggregations("access"),
            cases__project__project_id=get_schema_aggregations("cases__project__project_id"),
            file_size=get_schema_aggregations("file_size",schema_type="stats"))

        return file_aggregates

    def apply_whitelist(self, keep_list, store_fields):
        if keep_list:
            return list(keep_list.intersection(set(store_fields)))

    def get_sample_aggregations(self, samples):

        def get_stats_aggregations(variable_name):
            # do not serve buckets with just NA
            keys=list(aggregates[variable_name].keys())
            if len(keys) == 1 and keys[0] == "NA":
                return schema.Aggregations(
                           stats=schema.Stats(max=stats[variable_name].get("max",0), min=stats[variable_name].get("min",0)))
            else:
                return schema.Aggregations(
                           stats=schema.Stats(max=stats[variable_name].get("max",0), min=stats[variable_name].get("min",0)),
                           buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[variable_name].items()])

        sample_metadata_fields=utilities.order_metadata_keys(list(set(dir(samples[0])).difference(set(dir(schema.Sample())))), METADATA_SAMPLES_PROMOTE)
        demographic_metadata_fields=utilities.order_metadata_keys(list(set(dir(samples[0].demographic)).difference(set(dir(schema.Demographic())))), METADATA_DEMOGRAPHICS_PROMOTE)

        # if whitelist provided, then apply
        sample_metadata_fields=self.apply_whitelist(self.metadata_samples_whitelist,sample_metadata_fields)
        demographic_metadata_fields=self.apply_whitelist(self.metadata_demographics_whitelist,demographic_metadata_fields)

        # aggregate sample data
        aggregates = {"primary_site": {}, "project__project_id": {}, "project__program__name": {}}
        sample_lists = {}

        for demo_key in demographic_metadata_fields:
            aggregates["demographic__"+demo_key]={}

        stats = {}
        for key in sample_metadata_fields:
            aggregates[key]={}
            stats[key]={}
            sample_lists[key]=[]

        for sample in samples:
            for demo_key in demographic_metadata_fields:
                utilities.add_key_increment(aggregates["demographic__"+demo_key], getattr(sample.demographic, demo_key))

            utilities.add_key_increment(aggregates["primary_site"], sample.primary_site)
            utilities.add_key_increment(aggregates["project__project_id"], sample.project.project_id)
            utilities.add_key_increment(aggregates["project__program__name"], sample.project.program.name)

            for key in sample_metadata_fields:
                sample_lists[key].append(getattr(sample,key))

        # get the min/max/offset for each sample metadata
        self.compute_min_max_offset(stats, sample_metadata_fields, sample_lists)

        for key in sample_metadata_fields:
            for value in sample_lists[key]:
                utilities.add_key_increment(aggregates[key], utilities.Range.create(value,offset=stats[key].get("offset",1)))

        all_aggregations=[]
        for typename in sample_metadata_fields:
            if stats[typename].get("max",0) > 0:
                all_aggregations.append(schema.AggregationAnnotation(id="sample"+typename,metadataKey=typename,metadataType="stats",
                    metadataValue=schema.Aggregations(stats=schema.Stats(max=stats[typename].get("max",0), min=stats[typename].get("min",0)))))

        sample_aggregates=schema.SampleAggregations(
            metadataAggregations=schema.MetadataAggregations(hits=all_aggregations),
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__project_id"].items()]),
            project__program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__program__name"].items()]))

        for demo_key in demographic_metadata_fields:
            keys=list(aggregates["demographic__"+demo_key].keys())
            if not (len(keys) == 1 and keys[0] == "NA"):
                new_aggregations=schema.Aggregations(
                    buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__"+demo_key].items()])
                setattr(sample_aggregates,"demographic__"+demo_key, new_aggregations)

        for key in sample_metadata_fields:
            setattr(sample_aggregates, key, get_stats_aggregations(key))

        return sample_aggregates

    def get_metadata_title(self,field):
        if "demographic" in field:
            return field.split("demographic__")[-1]
        elif "program" in field:
            return "program"
        elif field.startswith("project"):
            return "project"
        elif field.startswith("sample"):
            return field.split("sample__")[-1]
        else:
            return field

    def compute_min_max_offset(self, stats, sample_metadata_fields, sample_lists, key_init=""):
        for key in sample_metadata_fields:
            try:
                stats[key_init+key]["max"]=max(filter(None,map(lambda x: float(x) if x.replace(".","").replace("-","").isdigit() else None, sample_lists[key])))
                stats[key_init+key]["min"]=min(filter(None,map(lambda x: float(x) if x.replace(".","").replace("-","").isdigit() else None, sample_lists[key])))
                stats[key_init+key]["offset"]=len(str(int(stats[key_init+key]["max"]-stats[key_init+key]["min"])))-1
            except ValueError:
                pass

    def get_case_aggregations(self, cases, filters):
        def get_schema_aggregations(variable_name):
            return schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[variable_name].items()])

        try:
            sample_metadata_fields=utilities.order_metadata_keys(list(set(dir(cases[0].samples.hits[0])).difference(set(dir(schema.Sample())))), METADATA_SAMPLES_PROMOTE)
            sample_metadata_fields=self.apply_whitelist(self.metadata_samples_whitelist,sample_metadata_fields)
        except IndexError:
            sample_metadata_fields=[]
        try:
            demographic_metadata_fields=utilities.order_metadata_keys(list(set(dir(cases[0].demographic)).difference(set(dir(schema.Demographic())))), METADATA_DEMOGRAPHICS_PROMOTE)
            demographic_metadata_fields=self.apply_whitelist(self.metadata_demographics_whitelist,demographic_metadata_fields)
        except IndexError:
            demographic_metadata_fields=[]

        # aggregate case data
        aggregates = {"primary_site": {}, "project__program__name": {}}
        
        stats={}
        demo_lists={}
        sample_lists={}
        for demo_key in demographic_metadata_fields:
            aggregates["demographic__"+demo_key]={}
            stats["demographic__"+demo_key]={}
            demo_lists[demo_key]=[]

        for key in sample_metadata_fields:
            aggregates["sample__"+key]={}
            stats["sample__"+key]={}
            sample_lists[key]=[]

        for case in cases:
            
            utilities.add_key_increment(aggregates["primary_site"], case.primary_site)
            utilities.add_key_increment(aggregates["project__program__name"], case.project.program.name)

            for demo_key in demographic_metadata_fields:
                demo_lists[demo_key].append(getattr(case.demographic, demo_key))


            for sample in case.samples.hits:
                for key in sample_metadata_fields:
                    sample_lists[key].append(getattr(sample,key))

        ## if not filters, then add programs without metadata
        if not filters:
            query = "select sum(total_participants) as total, program from project group by program"
            connection, db_results = self.query_database(query)
            total_participants={}
            for row in db_results:
                if not row['program'] in aggregates["project__program__name"]:
                    aggregates["project__program__name"][row['program']]=int(row['total'])

            connection.close()


        # compute min/max/offset
        self.compute_min_max_offset(stats, demographic_metadata_fields, demo_lists, "demographic__")
        self.compute_min_max_offset(stats, sample_metadata_fields, sample_lists, "sample__")

        for key in sample_metadata_fields:
            for value in sample_lists[key]:
                utilities.add_key_increment(aggregates["sample__"+key], utilities.Range.create(value,offset=stats["sample__"+key].get("offset",1)))

        for demo_key in demographic_metadata_fields:
            for value in demo_lists[demo_key]:
                utilities.add_key_increment(aggregates["demographic__"+demo_key], utilities.Range.create(value,offset=stats["demographic__"+demo_key].get("offset",1)))

        all_aggregations=[]
        for typename in ["project__program__name"]+list(map(lambda x: "demographic__"+x, demographic_metadata_fields))+list(map(lambda x: "sample__"+x, sample_metadata_fields)):
            # use only buckets if there are no min/max stats
            keys=list(aggregates[typename].keys())
            if (not typename in stats or stats[typename].get("max",0) == 0 or "sample" in typename):
                if not (len(keys) == 1 and keys[0] == "NA"):
                    all_aggregations.append(schema.AggregationAnnotation(id="case"+typename,metadataKey=typename,metadataType="bucket",metadataTitle=self.get_metadata_title(typename),
                        metadataValue=schema.Aggregations(buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[typename].items()])))

        for typename in list(map(lambda x: "demographic__"+x, demographic_metadata_fields)):
            if stats[typename].get("max",0) > 0:
                all_aggregations.append(schema.AggregationAnnotation(id="case"+typename,metadataKey=typename,metadataType="stats",metadataTitle=self.get_metadata_title(typename),
                    metadataValue=schema.Aggregations(buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[typename].items()],
                        stats=schema.Stats(max=stats[typename].get("max",0), min=stats[typename].get("min",0)))))

        case_aggregates=schema.CaseAggregations(
            metadataAggregations=schema.MetadataAggregations(hits=all_aggregations),
            primary_site=get_schema_aggregations("primary_site"),
            project__program__name=get_schema_aggregations("project__program__name"))

        for demo_key in demographic_metadata_fields:
            keys=list(aggregates["demographic__"+demo_key].keys())
            if not (len(keys) == 1 and keys[0] == "NA"):
                if stats["demographic__"+demo_key].get("max",0) > 0:
                    new_aggregations=schema.Aggregations(
                        stats=schema.Stats(max=stats["demographic__"+demo_key].get("max",0), min=stats["demographic__"+demo_key].get("min",0)),
                        buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__"+demo_key].items()])
                else:
                    new_aggregations=schema.Aggregations(
                        buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__"+demo_key].items()])
                setattr(case_aggregates,"demographic__"+demo_key, new_aggregations)

        for demo_key in sample_metadata_fields:
            keys=list(aggregates["sample__"+demo_key].keys())
            if not (len(keys) == 1 and keys[0] == "NA"):
                setattr(case_aggregates,"sample__"+demo_key, get_schema_aggregations("sample__"+demo_key))

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

