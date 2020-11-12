
# Calls to obtain values from the data structures, populated by the local cache database

import sqlalchemy
import sys
import time

import utilities
import schema

RAW_FILE_TYPE = "rawFiles"
PROCESSED_FILE_TYPE = "processedFiles"
GENERIC_FILE_NAME_OFFSET = 1000000

class Data(object):

    def __init__(self):
        # get the database environment variables
        username, password, database = utilities.get_database_variables()

        # create a pool of connections, pre-ping to prevent stale connections
        database_url = "mysql://{username}:{password}@localhost/{database}".format(username = username,
            password = password, database = database)

        try:
            self.engine = sqlalchemy.create_engine(database_url, pool_size=32, pool_pre_ping=True)
        except EnvironmentError as e:
            print("Unable to connect to local database")
            print("Database url {}".format(database_url))
            sys.exit(e)

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

    def valid_token(self, token):
        db_results = self.query_database("SELECT email, expires FROM users WHERE token='{}'".format(token), fetchall=True)
        if db_results:
            # check if the token has expired
            current_time = time.time()
            try:
                expires = float(db_results[0][1])
            except ValueError:
                expires = current_time
          
            if current_time > expires:
                db_results = self.query_database("UPDATE users SET token='{0}', expires='{1}' WHERE email='{2}'".format("None","None",db_results[0][0]), no_results=True)
                return False
            elif current_time < expires:
                return True
            else:
                return False
        else:
            return False

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
        for row in db_results:
            all_files.append(schema.File(id=row['file_id'], data_category=row['data_category'], experimental_strategy=row['experimental_strategy']))
            save_db_results.append(row)

        # apply filtering only for summary/file filters
        if filters:
            for content in filters["content"]:
                field=content["content"]["field"]
                if "summary" in field:
                    content["content"]["field"]="files."+field.split(".")[-1]
            filtered_files = utilities.filter_hits(all_files, filters, "files")
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

    @staticmethod
    def get_generic_file_name(file_id, extension):
        return "{0}.{1}".format(int(file_id)+GENERIC_FILE_NAME_OFFSET, extension.lower())

    def get_current_files(self):
        query = "SELECT file_sample.id as file_id, file_sample.file_id as file_url, file_sample.file_name as file_name, file_sample.participant, file_sample.sample, " +\
                 "file_sample.access, file_sample.file_size, file_sample.data_category, file_sample.data_format, " +\
                 "file_sample.platform, file_sample.experimental_strategy, file_sample.project, project.id as project_id, project.primary_site, " +\
                 "participant.id as participant_id, project.program, " +\
                 "participant.age as age, participant.weight_lbs as weight, participant.totMETs1 as met, " +\
                 "participant.caffiene as caffiene, participant.bmi as bmi, participant.alcohol as alcohol, participant.diagnosis as diagnosis, participant.pack_years_smoking as smoking, " +\
                 "sample.week as week, sample.Time as time, sample.drFiber as fiber, sample.drFat as fat, " +\
                 "sample.drB12 as b12, sample.drCalories as calories, sample.drCarbs as carbs, sample.drCholine as choline, " +\
                 "sample.drFolate as folate, sample.drProtein as protein, sample.weight_lbs as weight, " +\
                 "sample.non_ribosomal_proteins as non_ribosomal_proteins, sample.ribosomal_proteins as ribosomal_proteins, sample.totMETs1 as sample_met," +\
                 "sample.drIron as iron, sample.drAlcohol as alcohol, sample.id as sample_id " +\
                 "FROM file_sample INNER JOIN project ON file_sample.project=project.project_id " +\
                 "INNER JOIN participant ON file_sample.participant=participant.entity_participant_id "+\
                 "INNER JOIN sample on file_sample.sample=sample.sample"
        connection, db_results = self.query_database(query)
        files = []
        for row in db_results:
            metadataCase_hits=[]
            for demo_item in ['age','caffiene','bmi','alcohol','diagnosis','smoking','weight','met']:
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+demo_item,metadataKey=demo_item[0].upper()+demo_item[1:],metadataValue=row[demo_item]),

            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA', metadataCase_hits)))

            demographic_instance=schema.Custom()
            demographic_keys=['age','caffiene','bmi','alcohol','diagnosis','smoking','weight','met']
            schema.add_attributes(demographic_instance, demographic_keys, row)

            casesample_instance=schema.CaseSample(id=row['sample_id'])
            casesample_keys=['week','time','fiber','fat','iron','alcohol','b12','calories','carbs','choline','folate','protein','weight','met','non_ribosomal_proteins','ribosomal_proteins']
            schema.add_attributes(casesample_instance, casesample_keys, row)

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
                        id=row['participant_id'],
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
                        samples=[casesample_instance]
                        )]
                ),
                file_id=row['file_id'],
                type=row['data_format']
            ))
        connection.close()
        return files

    def get_current_samples(self):
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
        query = "SELECT sample.id as id, sample.sample as sample_name, participant.id as participant_id, " +\
                 "participant.entity_participant_id as participant_name, project.primary_site as primary_site, " +\
                 "project.id as project_id, project.project_id as project_name, project.program as program_name, " +\
                 "participant.age as age, participant.weight_lbs as weight, participant.totMETs1 as met, " +\
                 "participant.caffiene as caffiene, participant.bmi as bmi, participant.alcohol as alcohol, participant.diagnosis as diagnosis, participant.pack_years_smoking as smoking, " +\
                 "sample.week as week, sample.Time as time, sample.drFiber as fiber, sample.drFat as fat, " +\
                 "sample.drB12 as b12, sample.drCalories as calories, sample.drCarbs as carbs, sample.drCholine as choline, " +\
                 "sample.drFolate as folate, sample.drProtein as protein, sample.weight_lbs as weight, sample.totMETs1 as sample_met," +\
                 "sample.non_ribosomal_proteins as non_ribosomal_proteins, sample.ribosomal_proteins as ribosomal_proteins, " +\
                 "sample.drIron as iron, sample.drAlcohol as alcohol " +\
                 "FROM sample INNER JOIN participant ON sample.participant=participant.entity_participant_id " +\
                 "INNER JOIN project ON sample.project=project.project_id"
        connection, db_results = self.query_database(query)
        samples = []
        for row in db_results:
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
                    access=file_info['access'],
                    file_size=file_info['file_size']))

            metadataCase_hits=[]
            for demo_item in ['age','caffiene','bmi','alcohol','diagnosis','smoking','weight','met']:
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+demo_item,metadataKey=demo_item[0].upper()+demo_item[1:],metadataValue=row[demo_item]),

            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA', metadataCase_hits)))

            metadataSample_hits=[]
            for metadata_key in ['week','time','fiber','fat','iron','alcohol','b12','calories','carbs','choline','folate','protein','weight','sample_met','non_ribosomal_proteins','ribosomal_proteins']:
                metadataSample_hits.append(schema.MetadataSampleAnnotation(id=str(row['id'])+metadata_key,metadataKey=metadata_key.title(),metadataValue=row[metadata_key]))

            metadataSample_counts=len(list(filter(lambda x: x.metadataValue != 'NA', metadataSample_hits)))

            demographic_instance=schema.Custom()
            demographic_keys=['age','caffiene','bmi','alcohol','diagnosis','smoking','weight','met']
            schema.add_attributes(demographic_instance, demographic_keys, row)

            sample_instance=schema.Sample(
                id=row['id'],
                sample_id=row['sample_name'],
                primary_site=row['primary_site'],
                demographic=demographic_instance,
                metadataCase=schema.MetadataCase(
                    hits=metadataCase_hits,
                    metadata_count=metadataCase_counts),
                project=schema.Project(
                    id=row['project_id'],
                    project_id=row['project_name'],
                    name=row['project_name'],
                    program=schema.Program(name=row['program_name']),
                    primary_site=[row['primary_site']]),
                summary=summary,
                metadataSample=schema.MetadataSample(
                    hits=metadataSample_hits,
                    metadata_count=metadataSample_counts),
                files=schema.CaseFiles(hits=casefiles),
                cases=schema.FileCases(hits=[schema.FileCase(case_id=row['participant_id'], primary_site=row['primary_site'])])
            )

            sample_keys=['week','time','fiber','fat','iron','alcohol','b12','calories','carbs','choline','folate','protein','weight','non_ribosomal_proteins','ribosomal_proteins']
            schema.add_attributes(sample_instance, sample_keys, row)
            setattr(sample_instance, 'met', row['sample_met'])

            samples.append(sample_instance)
        connection.close()
        return samples


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

        # gather sample data for participants
        query = "SELECT id, participant, sample, week, Time as time, drFiber as fiber, " +\
                "drB12 as b12, drCalories as calories, drCarbs as carbs, drCholine as choline, " +\
                "drFolate as folate, drProtein as protein, weight_lbs as weight, " +\
                "non_ribosomal_proteins, ribosomal_proteins, totMETs1 as sample_met," +\
                "drFat as fat, drFiber as fiber, drIron as iron, drAlcohol as alcohol from sample"
        connection, db_results = self.query_database(query)
        case_samples = {}
        for row in db_results:
            if not row['participant'] in case_samples:
                case_samples[row['participant']] = []
            case_samples[row['participant']].append(dict(row.items()))
        connection.close()
        
        # gather participant data
        query = "SELECT participant.id as participant_id, participant.entity_participant_id as participant_name, project.primary_site as primary_site, " +\
                 "project.id as project_id, project.project_id as project_name, project.program as program_name, " +\
                 "participant.age as age, participant.weight_lbs as weight, participant.totMETs1 as met, " +\
                 "participant.caffiene as caffiene, participant.bmi as bmi, participant.alcohol as alcohol, participant.diagnosis as diagnosis, participant.pack_years_smoking as smoking " +\
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
                    access=file_info['access'],
                    file_size=file_info['file_size']))

            # create casesamples
            casesamples=[]
            for index, sample_info in enumerate(case_samples[row['participant_name']]):
                casesamples.append(schema.CaseSample(
                    id=index,
                    week=sample_info['week'],
                    time=sample_info['time'],
                    fiber=sample_info['fiber'],
                    iron=sample_info['iron'],
                    fat=sample_info['fat'],
                    alcohol=sample_info['alcohol'],
                    b12=sample_info['b12'],
                    calories=sample_info['calories'],
                    carbs=sample_info['carbs'],
                    choline=sample_info['choline'],
                    folate=sample_info['folate'],
                    protein=sample_info['protein'],
                    weight=sample_info['weight'],
                    met=sample_info['sample_met'],
                    non_ribosomal_proteins=sample_info['non_ribosomal_proteins'],
                    ribosomal_proteins=sample_info['ribosomal_proteins']))

            metadataCase_hits=[
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"age",metadataKey="Age",metadataValue=row['age']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"caffiene",metadataKey="Caffiene",metadataValue=row['caffiene']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"bmi",metadataKey="BMI",metadataValue=row['bmi']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"alcohol",metadataKey="Alcohol",metadataValue=row['alcohol']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"diagnosis",metadataKey="Diagnosis",metadataValue=row['diagnosis']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"smoking",metadataKey="Smoking",metadataValue=row['smoking']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"weight",metadataKey="Weight",metadataValue=row['weight']),
                schema.MetadataCaseAnnotation(id=str(row['participant_id'])+"met",metadataKey="MET",metadataValue=row['met'])]
            metadataCase_counts=len(list(filter(lambda x: x.metadataValue != 'NA', metadataCase_hits)))
            cases.append(schema.Case(
                id=row['participant_id'],
                case_id=row['participant_name'],
                primary_site=row['primary_site'],
                demographic=schema.Demographic(
                    age=row['age'],
                    weight=row['weight'],
                    caffiene=row['caffiene'],
                    bmi=row['bmi'],
                    alcohol=row['alcohol'],
                    diagnosis=row['diagnosis'],
                    smoking=row['smoking'],
                    met=row['met']),
                metadataCase=schema.MetadataCase(
                    hits=metadataCase_hits,
                    metadata_count=metadataCase_counts),
                project=schema.Project(
                    id=row['project_id'],
                    project_id=row['project_name'],
                    name=row['project_name'],
                    program=schema.Program(name=row['program_name']),
                    primary_site=[row['primary_site']]),
                summary=summary,
                files=schema.CaseFiles(hits=casefiles),
                samples=schema.CaseSamples(hits=casesamples),
            ))
            completed_cases.add(row['participant_id'])
        connection.close()
        return cases

    def get_cart_file_size(self, filters=None):
        all_files = self.get_current_files()
        filtered_files = utilities.filter_hits(all_files, filters, "files")
        # get the size from the filtered files
        total_size = sum([utilities.str_to_float([file.file_size], error_zero=True)[0] for file in filtered_files])
        return schema.CartSummaryAggs(fs=schema.FileSize(value=total_size))

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
            project = file.cases.hits[0].project
            utilities.add_key_increment(aggregates["cases__primary_site"], project.primary_site[0])
            utilities.add_key_increment(aggregates["cases__project__project_id"], project.project_id)

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

    def get_sample_aggregations(self, samples):

        def get_stats_aggregations(variable_name):
            return schema.Aggregations(
                       stats=schema.Stats(max=stats[variable_name].get("max",0), min=stats[variable_name].get("min",0)),
                       buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[variable_name].items()])

        # aggregate sample data
        aggregates = {"primary_site": {}, "project__project_id": {},
                      "project__program__name": {}, "demographic__age": {}, "demographic__weight": {}, "demographic__met": {} ,
                      "demographic__caffiene": {}, "demographic__bmi": {}, "demographic__alcohol": {} , "demographic__diagnosis": {}, "demographic__smoking": {} ,
                      "week" : {}, "time": {}, "fiber" : {}, "fat" : {}, "iron" : {}, "alcohol": {},
                      "b12": {}, "calories": {}, "carbs": {}, "choline" : {}, "folate" : {}, "protein": {}, "weight" : {}, "met" : {},
                       "non_ribosomal_proteins" : {}, "ribosomal_proteins": {} }
        stats = { "week": {}, "time": {}, "fiber" : {}, "fat" : {}, "iron" : {}, "alcohol": {}, "b12": {}, "calories": {}, "carbs": {},
                  "choline" : {}, "folate" : {}, "protein": {}, "weight" : {}, "met" : {}, "non_ribosomal_proteins" : {}, "ribosomal_proteins": {} }

        for sample in samples:
            utilities.add_key_increment(aggregates["demographic__age"], sample.demographic.age)
            utilities.add_key_increment(aggregates["demographic__weight"], sample.demographic.weight)
            utilities.add_key_increment(aggregates["demographic__caffiene"], sample.demographic.caffiene)
            utilities.add_key_increment(aggregates["demographic__bmi"], sample.demographic.bmi)
            utilities.add_key_increment(aggregates["demographic__alcohol"], sample.demographic.alcohol)
            utilities.add_key_increment(aggregates["demographic__diagnosis"], sample.demographic.diagnosis)
            utilities.add_key_increment(aggregates["demographic__smoking"], sample.demographic.smoking)
            utilities.add_key_increment(aggregates["demographic__met"], sample.demographic.met)
            utilities.add_key_increment(aggregates["primary_site"], sample.primary_site)
            utilities.add_key_increment(aggregates["project__project_id"], sample.project.project_id)
            utilities.add_key_increment(aggregates["project__program__name"], sample.project.program.name)
            utilities.add_key_increment(aggregates["week"], sample.week)
            utilities.add_key_increment(aggregates["time"], utilities.Range.create(sample.time))
            utilities.add_key_increment(aggregates["fiber"], sample.fiber)
            utilities.add_key_increment(aggregates["fat"], sample.fat)
            utilities.add_key_increment(aggregates["iron"], sample.iron)
            utilities.add_key_increment(aggregates["alcohol"], sample.alcohol)

            utilities.add_key_increment(aggregates["b12"],  utilities.Range.create_custom(sample.b12, offset=100))
            utilities.add_key_increment(aggregates["calories"], utilities.Range.create_custom(sample.calories, offset=100))
            utilities.add_key_increment(aggregates["carbs"],  utilities.Range.create_custom(sample.carbs, offset=100))
            utilities.add_key_increment(aggregates["choline"],  utilities.Range.create_custom(sample.choline, offset=100))
            utilities.add_key_increment(aggregates["folate"],  utilities.Range.create_custom(sample.folate, offset=100))
            utilities.add_key_increment(aggregates["protein"], sample.protein)
            utilities.add_key_increment(aggregates["weight"], sample.weight)
            utilities.add_key_increment(aggregates["met"], sample.met)
            utilities.add_key_increment(aggregates["non_ribosomal_proteins"], utilities.Range.create_custom(sample.non_ribosomal_proteins, offset=1000000))
            utilities.add_key_increment(aggregates["ribosomal_proteins"], utilities.Range.create_custom(sample.ribosomal_proteins, offset=1000000))


            utilities.update_max_min(stats["week"], sample.time)
            utilities.update_max_min(stats["time"], sample.time)
            utilities.update_max_min(stats["fiber"], sample.fiber)
            utilities.update_max_min(stats["fat"], sample.fat)
            utilities.update_max_min(stats["iron"], sample.iron)
            utilities.update_max_min(stats["alcohol"], sample.alcohol)

            utilities.update_max_min(stats["b12"], sample.b12)
            utilities.update_max_min(stats["calories"], sample.calories)
            utilities.update_max_min(stats["carbs"], sample.carbs)
            utilities.update_max_min(stats["choline"], sample.choline)
            utilities.update_max_min(stats["folate"], sample.folate)
            utilities.update_max_min(stats["protein"], sample.protein)
            utilities.update_max_min(stats["weight"], sample.weight)
            utilities.update_max_min(stats["met"], sample.met)
            utilities.update_max_min(stats["non_ribosomal_proteins"], sample.non_ribosomal_proteins)
            utilities.update_max_min(stats["ribosomal_proteins"], sample.ribosomal_proteins)


        all_aggregations=[]
        for typename in ["week","time","fiber","fat","iron","alcohol","b12","calories"]:
            all_aggregations.append(schema.AggregationAnnotation(id="sample"+typename,metadataKey=typename,metadataType="stats",
                metadataValue=schema.Aggregations(stats=schema.Stats(max=stats[typename].get("max",0), min=stats[typename].get("min",0)))))

        sample_aggregates=schema.SampleAggregations(
            metadataAggregations=schema.MetadataAggregations(hits=all_aggregations),
            demographic__age=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__age"].items()]),
            demographic__weight=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__weight"].items()]),
            demographic__caffiene=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__caffiene"].items()]),
            demographic__bmi=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__bmi"].items()]),
            demographic__alcohol=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__alcohol"].items()]),
            demographic__diagnosis=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__diagnosis"].items()]),
            demographic__smoking=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__smoking"].items()]),
            demographic__met=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__met"].items()]),
            primary_site=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["primary_site"].items()]),
            project__project_id=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__project_id"].items()]),
            project__program__name=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["project__program__name"].items()]),
            week=schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["week"].items()]),
            time=get_stats_aggregations("time"),
            fiber=get_stats_aggregations("fiber"),
            fat=get_stats_aggregations("fat"),
            iron=get_stats_aggregations("iron"),
            alcohol=get_stats_aggregations("alcohol"),

            b12=get_stats_aggregations("b12"),
            calories=get_stats_aggregations("calories"),
            carbs=get_stats_aggregations("carbs"),
            choline=get_stats_aggregations("choline"),
            folate=get_stats_aggregations("folate"),
            protein=get_stats_aggregations("protein"),
            weight=get_stats_aggregations("weight"),
            met=get_stats_aggregations("met"),
            non_ribosomal_proteins=get_stats_aggregations("non_ribosomal_proteins"),
            ribosomal_proteins=get_stats_aggregations("ribosomal_proteins"))

        return sample_aggregates

    def get_metadata_title(self,field):
        if "demographic" in field:
            return field.split("demographic__")[-1]
        elif field.startswith("project"):
            return "project"
        elif field.startswith("sample"):
            return field.split("sample__")[-1]
        else:
            return field

    def get_case_aggregations(self, cases):
        def get_schema_aggregations(variable_name):
            return schema.Aggregations(
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[variable_name].items()])

        # aggregate case data
        aggregates = {"primary_site": {}, "project__project_id": {},
                      "project__program__name": {}, "demographic__age": {}, "demographic__weight": {}, "demographic__met": {} ,
                      "demographic__caffiene": {}, "demographic__bmi": {}, "demographic__alcohol": {} , "demographic__diagnosis": {}, "demographic__smoking": {} ,
                      "sample__time" : {}, "sample__week" : {},  "sample__fiber" : {},  "sample__fat" : {},  "sample__iron" : {},  "sample__alcohol" : {},
                      "sample__b12" : {}, "sample__calories" : {}, "sample__carbs" : {}, "sample__choline": {}, "sample__folate" : {}, "sample__protein" : {},
                      "sample__weight" : {}, "sample__met": {}, "sample__non_ribosomal_proteins" : {}, "sample__ribosomal_proteins" : {}}

        stats = {"demographic__age": {}, "demographic__weight": {}, "demographic__met": {},
                 "demographic__caffiene": {}, "demographic__bmi": {}, "demographic__alcohol": {} , "demographic__diagnosis": {}, "demographic__smoking": {}  }

        for case in cases:
            utilities.add_key_increment(aggregates["demographic__age"], utilities.Range.create(case.demographic.age))
            utilities.add_key_increment(aggregates["demographic__weight"], utilities.Range.create_custom(case.demographic.weight, offset=25))
            utilities.add_key_increment(aggregates["demographic__caffiene"], utilities.Range.create_custom(case.demographic.caffiene, offset=25))
            utilities.add_key_increment(aggregates["demographic__bmi"], utilities.Range.create_custom(case.demographic.bmi, offset=10))
            utilities.add_key_increment(aggregates["demographic__alcohol"], utilities.Range.create_custom(case.demographic.alcohol, offset=10))
            utilities.add_key_increment(aggregates["demographic__diagnosis"], case.demographic.diagnosis)
            utilities.add_key_increment(aggregates["demographic__smoking"], utilities.Range.create_custom(case.demographic.smoking, offset=25))
            utilities.add_key_increment(aggregates["demographic__met"], utilities.Range.create_custom(case.demographic.met, offset=50))
            utilities.add_key_increment(aggregates["primary_site"], case.primary_site)
            utilities.add_key_increment(aggregates["project__project_id"], case.project.project_id)
            utilities.add_key_increment(aggregates["project__program__name"], case.project.program.name)
            utilities.update_max_min(stats["demographic__age"], case.demographic.age)
            utilities.update_max_min(stats["demographic__weight"], case.demographic.weight)
            utilities.update_max_min(stats["demographic__caffiene"], case.demographic.caffiene)
            utilities.update_max_min(stats["demographic__bmi"], case.demographic.bmi)
            utilities.update_max_min(stats["demographic__alcohol"], case.demographic.alcohol)
            utilities.update_max_min(stats["demographic__smoking"], case.demographic.smoking)
            utilities.update_max_min(stats["demographic__met"], case.demographic.met)
            for sample in case.samples.hits:
                utilities.add_key_increment(aggregates["sample__time"], utilities.Range.create(sample.time))
                utilities.add_key_increment(aggregates["sample__week"], sample.week)
                utilities.add_key_increment(aggregates["sample__fiber"], utilities.Range.create(sample.fiber))
                utilities.add_key_increment(aggregates["sample__fat"], utilities.Range.create(sample.fat))
                utilities.add_key_increment(aggregates["sample__iron"], utilities.Range.create(sample.iron))
                utilities.add_key_increment(aggregates["sample__alcohol"], utilities.Range.create(sample.alcohol))

                utilities.add_key_increment(aggregates["sample__b12"], utilities.Range.create_custom(sample.b12, offset=100))
                utilities.add_key_increment(aggregates["sample__calories"], utilities.Range.create_custom(sample.calories, offset=100))
                utilities.add_key_increment(aggregates["sample__carbs"], utilities.Range.create_custom(sample.carbs, offset=100))
                utilities.add_key_increment(aggregates["sample__choline"], utilities.Range.create_custom(sample.choline, offset=100))
                utilities.add_key_increment(aggregates["sample__folate"], utilities.Range.create_custom(sample.folate, offset=100))
                utilities.add_key_increment(aggregates["sample__protein"], utilities.Range.create(sample.protein))
                utilities.add_key_increment(aggregates["sample__weight"], utilities.Range.create(sample.weight))
                utilities.add_key_increment(aggregates["sample__met"], utilities.Range.create(sample.met))
                utilities.add_key_increment(aggregates["sample__non_ribosomal_proteins"], utilities.Range.create_custom(sample.non_ribosomal_proteins, offset=1000000))
                utilities.add_key_increment(aggregates["sample__ribosomal_proteins"], utilities.Range.create_custom(sample.ribosomal_proteins, offset=1000000))

        all_aggregations=[]
        for typename in ["project__program__name","demographic__diagnosis","sample__week","sample__time","sample__fiber","sample__fat","sample__iron","sample__alcohol","sample__b12","sample__calories","sample__carbs","sample__choline","sample__folate","sample__protein","sample__weight","sample__met"]:
            all_aggregations.append(schema.AggregationAnnotation(id="case"+typename,metadataKey=typename,metadataType="bucket",metadataTitle=self.get_metadata_title(typename),
                metadataValue=schema.Aggregations(buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[typename].items()])))

        for typename in ["demographic__age","demographic__weight","demographic__caffiene","demographic__bmi","demographic__met"]:
            all_aggregations.append(schema.AggregationAnnotation(id="case"+typename,metadataKey=typename,metadataType="stats",metadataTitle=self.get_metadata_title(typename),
                metadataValue=schema.Aggregations(buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates[typename].items()],
                    stats=schema.Stats(max=stats[typename].get("max",0), min=stats[typename].get("min",0)))))

        case_aggregates=schema.CaseAggregations(
            metadataAggregations=schema.MetadataAggregations(hits=all_aggregations),
            demographic__age=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__age"].get("max",0), min=stats["demographic__age"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__age"].items()]),
            demographic__weight=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__weight"].get("max",0), min=stats["demographic__weight"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__weight"].items()]),
            demographic__caffiene=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__caffiene"].get("max",0), min=stats["demographic__caffiene"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__caffiene"].items()]),
            demographic__bmi=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__bmi"].get("max",0), min=stats["demographic__bmi"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__bmi"].items()]),
            demographic__alcohol=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__alcohol"].get("max",0), min=stats["demographic__alcohol"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__alcohol"].items()]),
            demographic__smoking=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__smoking"].get("max",0), min=stats["demographic__smoking"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__smoking"].items()]),
            demographic__diagnosis=get_schema_aggregations("demographic__diagnosis"),
            demographic__met=schema.Aggregations(
                stats=schema.Stats(max=stats["demographic__met"].get("max",0), min=stats["demographic__met"].get("min",0)),
                buckets=[schema.Bucket(doc_count=count, key=key) for key,count in aggregates["demographic__met"].items()]),
            primary_site=get_schema_aggregations("primary_site"),
            project__project_id=get_schema_aggregations("project__project_id"),
            project__program__name=get_schema_aggregations("project__program__name"),
            sample__time=get_schema_aggregations("sample__time"),
            sample__week=get_schema_aggregations("sample__week"),
            sample__fiber=get_schema_aggregations("sample__fiber"),
            sample__fat=get_schema_aggregations("sample__fat"),
            sample__iron=get_schema_aggregations("sample__iron"),
            sample__alcohol=get_schema_aggregations("sample__alcohol"),

            sample__b12=get_schema_aggregations("sample__b12"),
            sample__calories=get_schema_aggregations("sample__calories"),
            sample__carbs=get_schema_aggregations("sample__carbs"),
            sample__choline=get_schema_aggregations("sample__choline"),
            sample__folate=get_schema_aggregations("sample__folate"),
            sample__protein=get_schema_aggregations("sample__protein"),
            sample__weight=get_schema_aggregations("sample__weight"),
            sample__met=get_schema_aggregations("sample__met"),
            sample__non_ribosomal_proteins=get_schema_aggregations("sample__non_ribosomal_proteins"),
            sample__ribosomal_proteins=get_schema_aggregations("sample__ribosomal_proteins"))

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
