#!/usr/bin/env python

""" This script loads samples and participants tables from google big query dataset,
and file sample information from FireCould workspaces  into local mariadb.
"""

import argparse
import subprocess
import sys
import copy
import os
import string
import query_firecloud
import query_bigquery

import utilities

def parse_arguments(args):
    """ Parse the arguments from the user """
    parser = argparse.ArgumentParser(
        description= "Loads google big query tables into local mariadb\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--project",
        default="biom-mass",
        help="google project name",
        required=False)
    parser.add_argument(
        "--dataset",
        default="HPFS_Demo_Clean",
        help="google big query dataset name",
        required=False)
    parser.add_argument(
        "--verbose",
        help="print each data set loaded to screen",
        action='store_true')
    parser.add_argument(
        "--file-participant",
        help="a file of participant data")
    parser.add_argument(
        "--file-sample",
        help="a file of sample data")
    parser.add_argument(
        "--delete-existing",
        help="delete all existing tables",
        action='store_true')

    return parser.parse_args()

def get_firecloud_data(verbose):

    all_samples,all_participants = query_firecloud.get_all_workspace_data(verbose)

    values_file_samples = list()
    values_participants = list()
    keys_file_samples = list()
    for samples in all_samples:
        for item in samples:
            participant_id=item['attributes']['participant']['entityName']
            del item['attributes']['participant']
            item['attributes']['participant'] = participant_id
            item['attributes']['entity_sample_id']=item['name']
            values_file_samples.append([str(i) for i in item['attributes'].values()])
            keys_file_samples.append([str(i) for i in item['attributes'].keys()])

    for participants in all_participants:
        for item in participants:
            values_participants.append(item['name'])

    # add more data based on the file url
    gs_folders=set()
    file_id_index=keys_file_samples[0].index('file_id')
    for index in range(len(values_file_samples)):
        file_url_info = values_file_samples[index][file_id_index].replace("gs://","").split("/")
        access = "open" if "public" in values_file_samples[index][file_id_index] else "controlled"
        data_category = file_url_info[3].lower()
        data_format = "fastq" if "fastq" in values_file_samples[index][file_id_index] else file_url_info[-1].split(".")[-1]
        experimental_strategy = file_url_info[2]
        file_name = file_url_info[-1]
        platform = file_url_info[1]
        gs_folders.add(os.path.dirname(values_file_samples[index][file_id_index]))
        filetype = "rawFiles" if data_format == "fastq" else "processedFiles"
        keys_file_samples[index]+=["access","data_category","data_format","experimental_strategy","file_name","platform","type"]
        values_file_samples[index]+=[access,data_category,data_format,experimental_strategy,file_name,platform,filetype]

    filetype_index=keys_file_samples[0].index('type')
    for index in range(len(values_file_samples)):
        # change the file bucket location to the download url and use the console page for raw files (so the user can naviate to UI instead of a direct download)
        if "raw" in values_file_samples[index][filetype_index]:
            values_file_samples[index][file_id_index]=os.path.dirname(values_file_samples[index][file_id_index].replace("gs://","https://console.cloud.google.com/storage/browser/"))
        else:
            values_file_samples[index][file_id_index]=values_file_samples[index][file_id_index].replace("gs://","https://storage.cloud.google.com/")

    return values_file_samples, keys_file_samples, values_participants

def delete_index(item_list, rm_index):
    new_item_list=[]
    for i, item in enumerate(item_list):
        if not i in rm_index:
            new_item_list.append(item)

    return new_item_list

def read_metadata_file(filename):
    rows = []
    with open(filename) as file_handle:
        column_names = file_handle.readline().rstrip()
        for line in file_handle:
            new_row=[]
            for item in line.rstrip().split(","):
                if item=="":
                    item="NA"
                new_row.append("'"+item+"'")
            rows.append(",".join(new_row))

        # allow for "NA" samples/participants in each project
        rows.append(",".join(["'NA'"]*len(new_row)))

    # check for any columns that are just NA
    col_remove_index=[]
    col_remove_names=[]
    for i, name in enumerate(column_names.split(",")):
        col_values=map(lambda x: x.split(",")[i], rows)
        if not list(filter(lambda x: x != "'NA'", map(lambda x: x.split(",")[i], rows))):
            col_remove_index.append(i)
            col_remove_names.append(name)

    # remove any columns if needed
    if col_remove_index:
        column_names=",".join(delete_index(column_names.split(","), col_remove_index))
        for i, current_row in enumerate(rows):
            rows[i]=",".join(delete_index(rows[i].split(","),col_remove_index))

        print("Removed metadata columns with out values (all NA): "+",".join(col_remove_names))

    return rows, column_names

def main():
    import mysql
    import mysql.connector as mariadb
    import datetime

    # parse arguments from the user
    args = parse_arguments(sys.argv)

    # get the database environment variables
    print("Getting local database settings")
    mysql_user, mysql_psw, local_db = utilities.get_database_variables()

    # get the location of the auth key (for firecloud and also google big query)
    # check for key here to prevent error with firecloud auth later
    try:
        key_file = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    except KeyError as e:
        print("Unable to find key file from env setting")
        sys.exit(e)

    # Get data from  big query
    if args.file_participant and args.file_sample:
        print("Reading data from local files")
        values_participant,columns_participant=read_metadata_file(args.file_participant)
        values_sample,columns_sample=read_metadata_file(args.file_sample)
    else:
        print("Calling Google BigQuery API")
        values_participant,values_sample,columns_participant,columns_sample=query_bigquery.query_bigquery(args.project,args.dataset,key_file,args.verbose)

    # Construct query to  create db in mariadb
    query_create_db = "CREATE DATABASE IF NOT EXISTS "+local_db

    # Construct query to  create table  participant in  mariadb
    columns_participant_desc = columns_participant.replace(","," varchar(100),")
    query_create_participant = '''CREATE TABLE IF NOT EXISTS
        participant(id int not null auto_increment primary key,'''
    query_create_participant =  query_create_participant + columns_participant_desc
    query_create_participant = query_create_participant + " varchar(100), updated timestamp)"

    # Construct query to create  table sample in mariadb
    columns_sample_desc = columns_sample.replace(","," varchar(100),")
    query_create_sample = '''CREATE TABLE IF NOT EXISTS
        sample(id int not null auto_increment primary key,
        project varchar(100),'''
    query_create_sample =  query_create_sample + columns_sample_desc
    query_create_sample = query_create_sample + ''' varchar(100),
        updated timestamp, 
        CONSTRAINT fk_participant FOREIGN KEY (participant)
        REFERENCES participant(entity_participant_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE)'''

    # Correct types for key fields  in create statements
    query_create_sample = query_create_sample.replace("sample varchar(100)","sample varchar(100) not null UNIQUE KEY")
    query_create_sample = query_create_sample.replace("participant varchar(100)","participant varchar(100) not null")
    query_create_participant = query_create_participant.replace(
        "entity_participant_id varchar(100)","entity_participant_id varchar(100) not null  UNIQUE KEY")
    if args.verbose:
        print(query_create_participant,query_create_sample)

    # Connect to mariadb
    print("Connecting to local database")
    mariadb_connection = mariadb.connect(user=mysql_user, password=mysql_psw)
    cursor = mariadb_connection.cursor(buffered=True)

    # Execute create db
    cursor.execute(query_create_db)
    mariadb_connection.commit()
    cursor.execute("USE " + local_db)
    mariadb_connection.commit()

    # Get the version of the existing database
    print("Get latest database version")
    try:
        cursor.execute("SELECT max(version) as maxversion, updated from  `version`")
        rows = cursor.fetchall()
    except mariadb.errors.ProgrammingError:
        rows = []
        prior_version = "NA"
        new_version = str(1.0)

    for maxversion, updated in rows:
        if maxversion:
           prior_version = maxversion
           new_version = str(float(str(maxversion)) + 0.1)
           if float(new_version) < 1.0:
               new_version = str(1.0)
        else:
           prior_version = "NA"
           new_version = str(1.0)
    print("** Prior database version was {}".format(prior_version))

    # Drop tables if exist
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    mariadb_connection.commit()

    if args.delete_existing:
        print("Dropping existing tables")
        cursor.execute("DROP TABLE IF EXISTS sample")
        cursor.execute("DROP TABLE IF EXISTS participant")
        cursor.execute("DROP TABLE IF EXISTS file_sample")
        cursor.execute("DROP TABLE IF EXISTS project")
        cursor.execute("DROP TABLE IF EXISTS version")
        mariadb_connection.commit()

    # Run create table participant statement
    cursor.execute(query_create_participant)
    mariadb_connection.commit()

    # Run  create table sample statement
    cursor.execute(query_create_sample)
    mariadb_connection.commit()

    # Construct and exxecute insert participants into mariadb participant statement
    for row in values_participant:
        insert_participant = "INSERT into participant (" + columns_participant + ") VALUES(" + row + ")"
        if args.verbose:
            print(insert_participant)
        try:
            cursor.execute(insert_participant)
        except mysql.connector.errors.IntegrityError:
            print("Duplicate entry for id: "+ row)
    mariadb_connection.commit()
    print("** {} total rows added to participant table".format(len(values_participant)))

    # Construct and execute insert samples into mariadb sample table
    for row in values_sample:
        insert_sample = "INSERT into sample (" + columns_sample + ") VALUES(" + row + ")"
        if args.verbose:
            print(insert_sample)
        cursor.execute(insert_sample)
    mariadb_connection.commit()
    print("** {} total rows added to sample table".format(len(values_sample)))

    # Get data from FireCloud workspaces
    values_file_samples,keys_file_samples,participants=get_firecloud_data(args.verbose)

    # Construct query to create table file_sample in mariadb
    columns_file_sample =','.join(keys_file_samples[0])
    columns_file_sample_desc = columns_file_sample.replace(","," varchar(100),")
    columns_file_sample_desc = columns_file_sample_desc.replace("file_id varchar(100),","file_id varchar(250),")

    query_create_file_sample = "CREATE TABLE IF NOT EXISTS file_sample(id int not null auto_increment primary key,\n"
    query_create_file_sample =  query_create_file_sample + columns_file_sample_desc
    query_create_file_sample = query_create_file_sample + ''' 
        varchar(100), updated timestamp,
        CONSTRAINT fsfk_participant FOREIGN KEY (participant)
        REFERENCES participant(entity_participant_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        CONSTRAINT fsfk_sample FOREIGN KEY (sample)
        REFERENCES sample(sample)
        ON DELETE CASCADE
        ON UPDATE CASCADE)'''
    query_create_file_sample = query_create_file_sample.replace(
        "entity_sample_id varchar(100)","entity_sample_id varchar(100) not null")
    query_create_file_sample = query_create_file_sample.replace("participant varchar(100)","participant varchar(100) not null")

    if args.verbose:
        print(query_create_file_sample)

    # Execure create table file_sample
    cursor.execute(query_create_file_sample)
    mariadb_connection.commit()

    # Construct and execute insert file samples into mariadb file_sample table
    for index in range(0,len(values_file_samples)):
        column_names = ','.join(keys_file_samples[index])
        row_values = ','.join("'" + str(e) + "'" for e in values_file_samples[index])
        insert_file_sample = "INSERT into file_sample (" + column_names + ") VALUES(" + row_values + ")"
        if args.verbose:
            print(insert_file_sample)
        cursor.execute(insert_file_sample)
    mariadb_connection.commit()
    print("** {} total rows added to file_sample table".format(len(values_file_samples)))

    # Update sample tables 'project' field
    project_index=keys_file_samples[0].index('project')
    sample_index=keys_file_samples[0].index('sample')
    for row in values_file_samples:
        update_sample_query="UPDATE sample set project='"+row[project_index]+"' where sample='"+row[sample_index]+"'"
        if args.verbose:
            print(update_sample_query)
        cursor.execute(update_sample_query)

    mariadb_connection.commit()

    # Construct and execute create project table statement
    query_create_project ='''CREATE TABLE IF NOT EXISTS
        project(id int not null auto_increment primary key,
        project_id varchar(100),
        name varchar(100),
        program  varchar(100),
        primary_site  varchar(100),
        updated timestamp)'''
    cursor.execute(query_create_project)
    mariadb_connection.commit()

    # Construct and execute insert into project
    cursor.execute("SELECT `project`,`sample` from `file_sample` GROUP BY `project`")
    rows = cursor.fetchall()

    for project, sample in rows:
        query_insert_project ='''INSERT INTO `project` (
           project_id,
           name,
           program,
           primary_site
           ) VALUES'''

        project_row_values ="('" + str(project) + "','" + str(project) + "'," + "'" + str(project.split("_")[0]) + "', 'Stool')"
        query_insert_project = query_insert_project +  project_row_values
        if args.verbose:
            print(query_insert_project)
        cursor.execute(query_insert_project)
    print("** {} total rows added to project table".format(len(rows)))

    mariadb_connection.commit()

    # Construct and execute create version table statement
    query_create_version ='''CREATE TABLE IF NOT EXISTS
        version(id int not null auto_increment primary key,
        commit varchar(250),
        data_release varchar(100),
        status varchar(10),
        tag varchar(10),
        version  varchar(10),
        updated timestamp)'''
    cursor.execute(query_create_version)
    mariadb_connection.commit()

    now = datetime.datetime.now()
    release_date ="Data Release v"+new_version+" - "+ now.strftime("%b %d, %Y")
    commit ="commit_"+now.strftime("%m%d%Y")
    query_insert_version ='''INSERT INTO `version` (
           commit,
           data_release,
           status,
           tag,
           version
           ) VALUES'''
    version_row_values ="('"+commit+"','"+release_date+"','OK','"+new_version+"','"+new_version+"')"
    query_insert_version = query_insert_version +  version_row_values
    if args.verbose:
        print(query_insert_version)
    cursor.execute(query_insert_version)
    mariadb_connection.commit()
    print("** New version table created with version {}".format(new_version))

    cursor.close()
    mariadb_connection.close()


if __name__ == "__main__":
    main()
