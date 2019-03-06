#!/usr/bin/env python

""" This script will take as input google big query dataset information and mariadb db information.
It will load samples and participants tables from google big query dataset into local mariadb.
"""

import argparse
import sys
import os
import string

def parse_arguments(args):
    """ Parse the arguments from the user """
    
    parser = argparse.ArgumentParser(
        description= "Loads google big query tables into local  mariadb\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--google-project", 
        default="biom-mass",
        help="google project name \n]", 
        required=False)
    parser.add_argument(
        "--private-key-file",
        default="biom-mass-fdcadb440fdf.json", 
        help="google project service account private key file path\n]", 
        required=False)
    parser.add_argument(
        "--gbq-dataset",
        default="HPFS_Demo", 
        help="google big query dataset name \n]", 
        required=False)
    parser.add_argument(
        "--local-db", 
        default="portal_ui",
        help="local mysql/mariadb database name \n", 
        required=False)
    parser.add_argument(
        "--mysql-user", 
        default="root",
        help="local mysql/mariadb user \n", 
        required=False)
    parser.add_argument(
        "--mysql-psw", 
        default="",
        help="local mysql/mariadb password \n", 
        required=False)
    
    return parser.parse_args()

def get_columns_query(project,dataset,table):
    # Construct query to get column names of table in big query
    # (big query does not support 'describe' statement)
    
    query = '''WITH EmptyReference AS (
        SELECT *
        FROM `'''
    query = query + project + "." + dataset
    query = query + "." + table + '''`  
        LIMIT 0
        )
        SELECT
        CONCAT(
        '',
        ARRAY_TO_STRING(
        REGEXP_EXTRACT_ALL(
        TO_JSON_STRING((SELECT AS STRUCT t.*)),
        r'"([^"]+)":'),
        ', '),
        '')
        FROM (
        SELECT AS VALUE t
        FROM EmptyReference AS t
        UNION ALL SELECT AS VALUE NULL
        ) AS t'''

    return query

def main():
    import mysql.connector as mariadb
    import google.cloud
    from google.cloud import bigquery

    # parse arguments from the user
    args = parse_arguments(sys.argv)

    client = bigquery.Client.from_service_account_json(args.private_key_file)
    # Construct query to select samples from big query sample
    QUERY_SAMPLE = 'SELECT * FROM `' + args.google_project +'.' + args.gbq_dataset + '.sample` '
    # Construct query to select participants from big query participant table 
    QUERY_PARTICIPANT = 'SELECT * FROM `' + args.google_project +'.' + args.gbq_dataset + '.participant`' 

    # Execute both queries 
    query_job_sample = client.query(QUERY_SAMPLE)
    query_job_participant = client.query(QUERY_PARTICIPANT)
    
    # Construct query to get column names of sample table in big query
    QUERY1 = get_columns_query(args.google_project,args.gbq_dataset,"sample")

    # Run query to get column names  of sample table 
    query1_job = client.query(QUERY1)
       
    for row in query1_job:
        dbcols1 = row[0]
        print(row[0])
    colslist1 = dbcols1.replace(",", " varchar(100),\n")
    print(colslist1)


    # Construct query to get columns of  participant table in big query
    QUERY2 = get_columns_query(args.google_project,args.gbq_dataset,"participant")

    # Run query to get columns  of participant table
    query2_job = client.query(QUERY2)
   
    for row in query2_job:
        dbcols2 = row[0]
        print(row[0])
    colslist2 = dbcols2.replace(",", " varchar(100),\n")
    print(colslist2)

    # Construct query to  create table  participant in  mariadb
    query_create = '''CREATE DATABASE IF NOT EXISTS portal_ui;
       USE portal_ui;'''
    query_create = '''CREATE TABLE IF NOT EXISTS participant(id int not null auto_increment primary key,\n'''
    query_create =  query_create + colslist2
    query_create_p = query_create + " varchar(100))\n"
    
    # Construct query to create  table sample in mariadb
    query_create = "CREATE TABLE IF NOT EXISTS sample(id int not null auto_increment primary key,\n"
    query_create =  query_create + colslist1
    query_create_s = query_create + ''' varchar(100),\n  CONSTRAINT fk_participant FOREIGN KEY (participant)
        REFERENCES participant(entity_participant_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE)'''

    # Correct types for key fields  in create statements
   
    qcreate_st = query_create_s.replace("sample varchar(100)","sample varchar(100) not null UNIQUE KEY")
    qcreate_sample = qcreate_st.replace("participant varchar(100)","participant int not null")
    qcreate_part = query_create_p.replace("entity_participant_id varchar(100)","entity_participant_id int not null  UNIQUE KEY")
    print(qcreate_part,qcreate_sample)

    # Connect to mariadb
    mariadb_connection = mariadb.connect(user=args.mysql_user, password=args.mysql_psw, database=args.local_db)
    cursor = mariadb_connection.cursor()

    # Run create table participant statement
    cursor.execute(qcreate_part)
    mariadb_connection.commit()

    # Run  create table sample statement
    cursor.execute(qcreate_sample)
    mariadb_connection.commit()

    # Construct insert participants into mariadb participant statement 
    for row in query_job_participant:
        qvalues = ','.join("'" + str(e) + "'" for e in row)
        print qvalues
        insert_part = "INSERT into participant (" + dbcols2 + ") VALUES(" + qvalues + ")"
        print(insert_part)
        cursor.execute(insert_part)
    mariadb_connection.commit()
    
    #Construct insert samples into mariadb sample table
    for row in query_job_sample:
        qvalues = ','.join("'" + str(e) + "'" for e in row)
        print qvalues
        insert_sample = "INSERT into sample (" + dbcols1 + ") VALUES(" + qvalues + ")"
        print(insert_sample)
        cursor.execute(insert_sample)
    mariadb_connection.commit()

if __name__ == "__main__":
    main()
