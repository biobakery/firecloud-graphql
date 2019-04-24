FROM mariadb

COPY *.py /usr/local/src/

RUN apt-get update && apt-get install -y python build-essential python-dev python-pip python-setuptools python-mysqldb

# use older firecloud version to resolve new issue with auth
RUN pip install firecloud==0.16.20 graphene flask flask-graphql flask-cors sqlalchemy

RUN pip install mysql-connector-python

RUN pip install --upgrade google-cloud-bigquery

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/src/keys/biom-mass-8dc9ab934396.json
COPY ./keys/biom-mass-8dc9ab934396.json $GOOGLE_APPLICATION_CREDENTIALS

CMD ["mysqld"]
