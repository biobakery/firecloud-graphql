FROM mariadb:10.2.23-bionic

COPY *.py /usr/local/src/

RUN apt-get update && apt-get install -y python build-essential python-dev python-pip python-setuptools python-mysqldb

# use older firecloud version to resolve new issue with auth
RUN pip install firecloud==0.16.20 graphene flask flask-graphql flask-cors sqlalchemy

RUN pip install mysql-connector-python

RUN pip install google-cloud-bigquery==1.24.0

# roll back google packages to those that are compatible with firecloud version
RUN pip install google-api-core==1.17.0 google-auth==1.14.1 google-cloud-core==1.3.0 google-resumable-media==0.5.0 googleapis-common-protos==1.51.0

# install gsutil for service account
RUN pip install gsutil==4.53

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/src/keys/biom-mass-293819-c94fb7976032.json
COPY ./keys/biom-mass-293819-c94fb7976032.json $GOOGLE_APPLICATION_CREDENTIALS
COPY ./keys/biom-mass-293819-dbd067ad4a3b.json /usr/local/src/keys/

CMD ["mysqld", "--wait_timeout=28800"]
