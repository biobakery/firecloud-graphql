#!/usr/bin/env python

""" This script loads samples and participants tables from google big query dataset,
and file sample information from FireCould workspaces  into local mariadb.
"""

import argparse
import sys
import os
import string
import query_firecloud
import query_bigquery

def parse_arguments(args):
    """ Parse the arguments from the user """
    parser = argparse.ArgumentParser(
        description= "Loads google big query tables into local  mariadb\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--project",
        default="biom-mass",
        help="google project name \n]",
        required=False)
    parser.add_argument(
        "--key-file",
        default="/home/hutlab_public/compute_engine_service_account_key/biom-mass-8dc9ab934396.json",
        help="google project service account private key file path\n]",
        required=False)
    parser.add_argument(
        "--dataset",
        default="HPFS_Demo_Clean",
        help="google big query dataset name \n]",
        required=False)
    parser.add_argument(
        "--local-db",
        default="portal_ui",
        help="local mysql/mariadb database name \n",
        required=False)
    parser.add_argument(
        "--mysql-user",
        default="biom_mass",
        help="local mysql/mariadb user \n",
        required=False)
    parser.add_argument(
        "--mysql-psw",
        help="local mysql/mariadb password \n",
        required=True)

    return parser.parse_args()

def get_firecloud_data():

    all_samples,all_participants = query_firecloud.get_all_workspace_data()

    values_file_samples = list()
    values_participants = list()
    keys_file_samples = list()
    for samples in all_samples:
        for item in samples:
            participant_id=item['attributes']['participant']['entityName']
            del item['attributes']['participant']
            item['attributes']['participant'] = participant_id
            item['attributes']['entity_sample_id']=item['name']
            values_file_samples.append(item['attributes'].values())
            keys_file_samples.append(item['attributes'].keys())

    for participants in all_participants:
        for item in participants:
            values_participants.append(item['name'])

    return values_file_samples, keys_file_samples, values_participants

def main():
    import mysql.connector as mariadb
    import datetime

    # parse arguments from the user
    args = parse_arguments(sys.argv)

    # Get data from  big query
    values_participant,values_sample,columns_participant,columns_sample=query_bigquery.query_bigquery(args.project,args.dataset,args.key_file)

    # Construct query to  create db in mariadb
    query_create_db = "CREATE DATABASE IF NOT EXISTS "+args.local_db

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
    print(query_create_participant,query_create_sample)

    # Connect to mariadb
    mariadb_connection = mariadb.connect(user=args.mysql_user, password=args.mysql_psw)
    cursor = mariadb_connection.cursor(buffered=True)

    # Execute create db
    cursor.execute(query_create_db)
    mariadb_connection.commit()
    cursor.execute("USE " + args.local_db)
    mariadb_connection.commit()

    # Drop tables if exist
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    mariadb_connection.commit()

    cursor.execute("DROP TABLE IF EXISTS sample")
    cursor.execute("DROP TABLE IF EXISTS participant")
    cursor.execute("DROP TABLE IF EXISTS file_sample")
    cursor.execute("DROP TABLE IF EXISTS project")
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
        print(insert_participant)
        cursor.execute(insert_participant)
    mariadb_connection.commit()

    # Construct and execute insert samples into mariadb sample table
    for row in values_sample:
        insert_sample = "INSERT into sample (" + columns_sample + ") VALUES(" + row + ")"
        print(insert_sample)
        cursor.execute(insert_sample)
    mariadb_connection.commit()

    # Get data from FireCloud workspaces
    values_file_samples,keys_file_samples,participants=get_firecloud_data()

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

    print(query_create_file_sample)

    # Execure create table file_sample
    cursor.execute(query_create_file_sample)
    mariadb_connection.commit()

    # Construct and execute insert file samples into mariadb file_sample table
    for index in range(0,len(values_file_samples)):
        column_names = ','.join(keys_file_samples[index])
        row_values = ','.join("'" + str(e) + "'" for e in values_file_samples[index])
        insert_file_sample = "INSERT into file_sample (" + column_names + ") VALUES(" + row_values + ")"
        print(insert_file_sample)
        cursor.execute(insert_file_sample)
    mariadb_connection.commit()

    # Update sample tables  'project' field
    for row in values_file_samples:
        update_sample_query="UPDATE sample set project='"+row[3]+"' where sample='"+row[6]+"'"
        print(update_sample_query)
        cursor.execute(update_sample_query)

    mariadb_connection.commit()

    # Construct and execute create project table statement
    query_create_project ='''CREATE TABLE IF NOT EXISTS
        project(id int not null auto_increment primary key,
        project_id varchar(100),
        name varchar(100),
        program  varchar(100),
        summary  varchar(250),
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
           summary,
           primary_site
           ) VALUES'''

        project_row_values ="('" + str(project) + "','" + str(project) + "'," + "'HPFS','Project Summary', 'Stool')"
        query_insert_project = query_insert_project +  project_row_values

        print(query_insert_project)
        cursor.execute(query_insert_project)

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

    # Construct and execute insert into version
    cursor.execute("SELECT max(version) as maxversion, updated from  `version`")
    rows = cursor.fetchall()

    for maxversion, updated in rows:
        if maxversion:
           new_version = str(float(str(maxversion)) + 0.1)
        else:
           new_version = str(0.1)

    now = datetime.datetime.now()
    release_date ="Data Release "+new_version+" - "+ now.strftime("%b %d, %Y")
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
    print(query_insert_version)
    cursor.execute(query_insert_version)
    mariadb_connection.commit()

    cursor.close()
    mariadb_connection.close()


    print("--All data loaded---")

if __name__ == "__main__":
    main()
