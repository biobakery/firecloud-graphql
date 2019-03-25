#!/usr/bin/env python

""" This script queries google big query dataset.
It takes as an argument google project, big query dataset name, credentials key.
"""

import argparse
import sys
import os
import string

def parse_arguments(args):
    """ Parse the arguments from the user """
    
    parser = argparse.ArgumentParser(
        description= "Queries google big query dataset\n",
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

def query_bigquery(project, dataset, key):

    import google.cloud
    from google.cloud import bigquery

    # Define big query client instance
    client = bigquery.Client.from_service_account_json(key)

    # Construct query to select samples from big query sample
    QUERY_SAMPLE = 'SELECT * FROM `' + project +'.' + dataset + '.sample` '

    # Construct query to select participants from big query participant table 
    QUERY_PARTICIPANT = 'SELECT * FROM `' + project +'.' + dataset + '.participant`' 

    # Execute both queries 
    query_sample_job = client.query(QUERY_SAMPLE)
    query_participant_job = client.query(QUERY_PARTICIPANT)
    
    # Construct query to get column names of sample table in big query
    QUERY_SAMPLE_COLS = get_columns_query(project,dataset,"sample")

    # Run query to get column names of sample table 
    query_sample_cols_job = client.query(QUERY_SAMPLE_COLS)
       
    for row in query_sample_cols_job:
        columns_sample = row[0]
        print("Sample column", columns_sample, "\n")

    # Construct query to get columns of  participant table in big query
    QUERY_PART_COLS = get_columns_query(project,dataset,"participant")

    # Run query to get columns  of participant table
    query_part_cols_job = client.query(QUERY_PART_COLS)
    for row in query_part_cols_job:
        columns_participant = row[0]
        print("Participant column", columns_participant, "\n")
   
    # Get participant values 
    values_participant = list()
    for row in query_participant_job:
        values_participant_row = ','.join("'" + str(e)+ "'" for e in row)
        print ("Participant row",values_participant_row, "\n")
        values_participant.append(values_participant_row)

    
    # Get sample values
    values_sample = list()
    for row in query_sample_job:
        values_sample_row = ','.join("'" + str(e)+ "'" for e in row)
        print ("Sample row", values_sample_row, "\n")
        values_sample.append(values_sample_row)

    return values_participant, values_sample, columns_participant, columns_sample

if __name__ == "__main__":
    
    args = parse_arguments(sys.argv)
    query_bigquery(args.project, args.dataset, args.key_file)
