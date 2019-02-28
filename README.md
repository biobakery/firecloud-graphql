
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

#### Installation 

A registered service account must be set up prior to using the Firecloud API script. 

Follow these steps to set up an account registered with Firecloud:

1. In Google Cloud go to IAM -> Service accounts (and create a new service account or use the existing compute if running on a VM) and create a key.
2. Download this key to the machine you will run the Firecloud API script.
3. Install firecloud-tools and run the following command (replacing $PATH_TO_KEY and $EMAIL with specific values)
```
$ ./run.sh scripts/register_service_account/register_service_account.py -j $PATH_TO_KEY -e $EMAIL
```
4. Set the environment variable to point to the KEY
```
$ export GOOGLE_APPLICATION_CREDENTIALS=$PATH_TO_KEY
```
5. Login to the account (if not using a compute engine service account on a VM) with `gsutil config`

When running the Firecloud API script make sure the environment variable is set and firecloud-tools, plus all of its dependencies are installed.

#### Run

[TBD]

### BigQuery API

#### Installation

[TBD, describe authentication setup]

#### Run

[TBD]
