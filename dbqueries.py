#  This file holds all queries run in database.py



all_counts_query='''select count(id) as total from project
                    union all select count(id) as total from participant
                    union all select count(id) as total from sample
                    union all select count(distinct data_format) as total from file_sample
                    union all select count(id) as total from file_sample where  type="rawFiles"
                    union all select count(id) as total from file_sample where type="processedFiles"'''
projects_query="select id from project"
version_query="select * from version order by updated desc limit 1"
files_query="select id from file_sample"
cases_query="select id from participant"
files_size_query="select sum(file_size) as sum_size from  file_sample"
files_total_query="select count(id) as total from file_sample"
cases_total_query="select count(distinct id) as total from participant"

def project_query(p_id):
    return "select * from project where  id =" + str(p_id)

def project_counts_query(p_id):
    query="select count(id) as total from  file_sample where project='"+p_id+"'"
    query=query+" union all "
    query=query+"select count(distinct participant) as total from file_sample where project='"+p_id+"'"
    query=query+" union all "
    query=query+"select sum(file_size) as total from file_sample where project='"+p_id+"'"
    return query

def data_cat_query(table, p_id):
    return "select distinct data_category from file_sample where "+ table+"='" + str(p_id)+"'"

def data_cat_counts_query(table,p_id,data_cat):
    query="select count(id) as total from file_sample where data_category='"+data_cat+"' and "+table+"='"+str(p_id)+"'"
    query=query+" union all "
    query=query+"select count(distinct participant) as total from file_sample where data_category='"+data_cat+"' and "+table+"='"+str(p_id)+"'"
    return query

def exp_str_query(table,p_id):
    return "select distinct experimental_strategy from file_sample where "+ table+"='" + str(p_id) +"'"

def exp_str_counts_query(table,p_id,exp_str):
    query="select count(id) as total from file_sample where experimental_strategy='"+exp_str+"' and "+table+"='"+str(p_id)+"'"
    query=query+" union all "
    query=query+ "select count(distinct participant) as total from file_sample where experimental_strategy='"+exp_str+"' and "+table+"='"+str(p_id)+"'"
    return query

def file_query(f_id):
    query='''select file_sample.*,
                      project.id as p_id, project.project_id as proj_id,project.primary_site,
                      participant.id as part_id
                      from file_sample,project,participant where file_sample.id='''+str(f_id)
    query=query+''' and file_sample.project=project.project_id and
                                  file_sample.participant=participant.entity_participant_id'''
    return query

def case_query(p_id):
     return '''select participant.entity_participant_id, file_sample.id, file_sample.experimental_strategy,
               file_sample.data_category, file_sample.platform, file_sample.access,file_sample.data_format
               from participant, file_sample
               where participant.id='''+str(p_id)+" and file_sample.participant=participant.entity_participant_id"

def case_counts_query(p_id):
    query="select count(id) as total from participant where entity_participant_id="+str(p_id)
    query=query+" union all "
    query=query+ "select count(id) as total from file_sample where participant="+str(p_id)
    query=query+" union all "
    query=query+"select sum(file_size) as total from file_sample where participant="+str(p_id)
    return query

def case_project_query(p_id):
    query="select distinct file_sample.project, project.id as p_id, project.primary_site "
    query=query+"from file_sample, project where file_sample.participant='"
    query=query+str(p_id)+"' and project.project_id=file_sample.project limit 1"
    return query


def metadata_part_query(p_id):
    return "select * from participant where entity_participant_id="+str(p_id)

def metadata_sample_query(p_id):
    return "select * from sample where participant="+str(p_id)

