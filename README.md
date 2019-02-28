
# Firecloud GraphQl

## GraphQL Server

To install: 
`` $ pip install firecloud flask graphene>=2.0.0 flask-graphql ``

* Also [firecloud-tools](https://github.com/broadinstitute/firecloud-tools) are required for the Firecloud API queries.

To run:
`` $ python server.py ``

The file named `schema.graphql` contains the current schema (implemented in the module of the same name). Use the data utility script in the Portal UI repository to update this schema when needed.

## External API Utilities

The server will load data from a local database. This database is created by running a utility script which queries
the Firecloud and BigQuery APIs.

### Firecloud API

[TBD]

### BigQuery API

[TBD]
