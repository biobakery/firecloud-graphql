
# Basic server to host graphql with flask on localhost:5000
# Interfaces to firecloud api

# The initial server was based on the core framework from the example code from
# https://github.com/nderkach/python-grahql-api
# which wraps an end point of the RESTful AirBnB API with GraphQl.
# Code from the example is included in the utilities functions.

import os

import flask
import flask_cors
import flask_graphql
import graphene

from google.oauth2 import id_token
from google.auth.transport import requests

import logging

import schema
from database import data

# set the name of the log file
access_log_file=os.path.join(os.path.dirname(__file__),"logs","server.log")

# configure the logger
logging.basicConfig(filename=access_log_file,format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    level='INFO', filemode='a', datefmt='%m/%d/%Y %I:%M:%S %p')


NAME = "firecloud_graphql"
HOST = "0.0.0.0"
PORT = "5000"
GOOGLE_AUDIENCE = "250496797473-15s2p3k9s7latehllsj4o2cv5qp1jl1c.apps.googleusercontent.com"
#GOOGLE_AUDIENCE = "250496797473-3tkrt8bluu5l508kik1j2ufurpiamgsn.apps.googleusercontent.com"

GOOGLE_COOKIE_NAME = "google_access_token"


def verify_user(token):
    # verify the user token is a valid google oauth2 token
    request = requests.Request()

    try:
        token_info = id_token.verify_token(
            token, request, GOOGLE_AUDIENCE)
    except ValueError:
        token_info = {'iss': ""}

    # check this has the correct issuer
    if token_info['iss'] != "accounts.google.com":
        return token, "", "no"
    else:
        return token, token_info["email"], "yes"

def process_query(request, schema_query):
    # process the request from the url
    url_hash=request.args.get("hash")
    data_body=request.get_json()
    data_query=data_body["query"]
    data_variables=data_body.get("variables",{})

    # get token
    token_cookie=request.cookies.get(GOOGLE_COOKIE_NAME,"")

    firecloud_schema=graphene.Schema(query=schema_query, auto_camelcase=False)
    result=firecloud_schema.execute(data_query, variables=data_variables)
    if result.errors:
        print("ERROR")
        print(data_query)
        print(data_variables)
        print(result.errors)

    # filter out items that should not be servered without auth
    schema.filter_noauth(result.data)

    json_result=flask.jsonify({"data": result.data})

    return json_result

def main():
    # create the graphql flask app
    app = flask.Flask(NAME)
    # allow initial OPTIONS requests
    flask_cors.CORS(app)

    # add the root graphql queries
    @app.route('/graphql', methods=["POST"])
    def get_root_schema():
        return process_query(flask.request, schema.Query)

    # add subdirectories to identify schema
    @app.route('/graphql/<name>', methods=["POST"])
    def get_schema(name):
        return process_query(flask.request, schema.Query)

    # add static endpoint for version/status
    @app.route('/status', methods=["GET"])
    def get_version():
        return flask.jsonify(data.get_version())

    # add static endpoint for access
    @app.route('/access', methods=["POST"])
    def get_access():
        data_body=flask.request.get_json()
        hash_token, email, access = verify_user(data_body["token"])
        if access == "yes":
            logging.info("Access GRANTED for user: " + email)
        else:
            logging.info("Access DENIED for user request from email: " + data_body["email"])
        return flask.jsonify({ "hash_token": hash_token,"access": access })

    # add end point for graphql gui
    app.add_url_rule('/test', view_func=flask_graphql.GraphQLView.as_view(
        'test', schema=graphene.Schema(query=schema.Query, auto_camelcase=False), graphiql=True))

    # start the app
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
