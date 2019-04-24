
# Firecloud GraphQl

## GraphQL Server

To install: 
`` $ pip install firecloud flask graphene>=2.0.0 flask-graphql flask-cors sqlalchemy``

* Also [firecloud-tools](https://github.com/broadinstitute/firecloud-tools) are required for the Firecloud API queries.

To run:
`` $ python server.py ``

The file named `schema.graphql` contains the current schema (implemented in the module of the same name). Use the data utility script in the Portal UI repository to update this schema when needed.

## External API Utilities

The server will load data from a local database. This database is created by running a utility script which queries the Firecloud and BigQuery APIs.

### Run 

The script that loads the local database with data from the Firecloud workspaces and BigQuery database is run as follows.

``python load_local_database.py``

Script calls functions from other 2 scripts query_firecloud.py and query_bigquery.py. These 2 scripts can be run to view data in Firecloud and BigQuery

Before running the script first set up the environment for the external API calls and have mariadb running. This script requires the same three
environment variables to query the local database as the server.

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
6. Add the service account to each Firecloud workspace it will need to query. This can be done by adding the service account email id to the "Share" page as a new "User ID" with READER level access (no share and no compute permissions).

When running the Firecloud API script make sure the environment variable is set and firecloud-tools, plus all of its dependencies are installed.

### BigQuery API

#### Installation

To install the client library run

``pip install --upgrade google-cloud-bigquery``

To set up authentication

1. In the Google Console of your project create service account
2. Download generated json file that contains your credentials key
3. Either set path to your credentials file as environmental variable

 ``export GOOGLE_APPLICATION_CREDENTIALS=$PATH_TO_KEY``
  
  or pass path directly when defining client within code
  
 ``from google.cloud import bigquery``
 ``client = bigquery.Client.from_service_account_json($PATH_TO_KEY)``
 
 More information 
 https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python
 
## Data Repositories

### BigQuery Dataset

Biom-mass project Demo dataset 'HPFS_Demo_Clean' has 2 tables

1. participant (has all fileds that describe participant of study)
2. sample (has all fileds that describe measurements/tests taken on participant during study

sample table has participant field that connects it to participant by id.

### Firecloud Workspaces

Firecloud workspaces have

1. All raw files and processed files of study uploaded to google backet associated with workspace
2. Information about files is stored as key/value pairs in 'sample' section

access 
data_category
data_format
experimental_strategy
file_id
file_name
file_size
participant
platform
sample
type

3. Participant ids are stored in 'participant' section of workspace

Files and related information are associated to participants by key 'participant' that matches participant id.

### Local Maria DB

Local to portal mariadb combines all data from BigQuery and Firecloud Workspaces and stores information in 3 tables

1. participant (all participant information from BigQuery)
2. sample (all sample information from BigQuery)
3. file_sample (all file information from all Firecloud Workspaces)

file_sample and sample tables have 'participant' field that connects them to participant table by id.

To install mariadb on ubuntu/debian run

``sudo apt-get update -y``
``sudo apt-get install mariadb-server mariadb-client``

To set root password (it is none by default) run

``sudo mysql_secure_installation`` 

More information
https://websiteforstudents.com/students-tutorial-install-mariadb-ubuntu-16-10/


To create non root user in mysql  login as root user
``sudo mysql --user=root -p``
then run
1. ``CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';``
2. ``GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;``
3. ``flush privileges;``

More information https://dev.mysql.com/doc/refman/5.5/en/adding-users.html

load_local_database.py script needs mysql.connect module.

To install run
``pip install mysql-connector-python``


## Production

This server runs in a docker container that is hosted by nginx running in the portal-ui container. 

To build: `$ sudo docker sudo docker build -t graphql . `

To run: `$ sudo docker run -d --name graphql -e MYSQL_ROOT_PASSWORD=biobakery -e MYSQL_USER=biom_mass -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=portal_ui -p 5000:5000 -v /opt/database:/var/lib/mysql graphql`

When running a new container replace passwords in demo command above. This command will reuse the existing database at /opt/database.

To start:
```
$ sudo docker exec -it graphql bash
$ cd /usr/local/src
$ python load_local_database.py (if needed as based on prior db with mount)
$ nohup python server.py > server.log &
```
