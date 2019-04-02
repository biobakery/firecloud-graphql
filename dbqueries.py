#  This file holds all queries run in database.py
all_counts_query='''select count(id) as total from project
                    union all select count(id) as total from participant
                    union all select count(id) as total from sample
                    union all select count(distinct data_format) as total from file_sample
                    union all select count(id) as total from file_sample where  type="rawFiles"
                    union all select count(id) as total from file_sample where type="processedFiles"'''

version_query="select * from version order by updated desc limit 1"
