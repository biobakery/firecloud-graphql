
# Firecloud GraphQl

## GraphQL Server

To install: 
`` $ pip install firecloud flask graphene>=2.0.0 flask-graphql ``

* Also [firecloud-tools](https://github.com/broadinstitute/firecloud-tools) are required for the Firecloud API queries.

To run:
`` $ python server.py ``

* Also if using install with virtual env source it first ( server requires firecloud tools to be installed )
* `$ source ~/firecloud-tools/.firecloud-tools/venv/bin/activate `

## External API Utilities

The server will load data from a local database. This database is created by running a utility script which queries
the Firecloud and BigQuery APIs.

### Firecloud API



### BigQuery API
