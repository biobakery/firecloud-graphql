
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

import hashlib
import binascii

import logging

import schema
from database import Data

# set the name of the log file
access_log_file=os.path.join(os.path.dirname(__file__),"logs","server.log")

# configure the logger
logging.basicConfig(filename=access_log_file,format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    level='INFO', filemode='a', datefmt='%m/%d/%Y %I:%M:%S %p')


NAME = "firecloud_graphql"
HOST = "0.0.0.0"
PORT = "5000"

GOOGLE_AUDIENCE = "257500970741-c4cufvq18ts3r3sdvl3u8l5ibqis8s3b.apps.googleusercontent.com"
#GOOGLE_AUDIENCE = "250496797473-3tkrt8bluu5l508kik1j2ufurpiamgsn.apps.googleusercontent.com"

GOOGLE_COOKIE_NAME = "biom_mass_token"

def hash_access_token(token):
    # get the hash of the access token
    hash = hashlib.pbkdf2_hmac('sha256', bytes(token), bytes(os.urandom(16)), 100000)
    
    return binascii.hexlify(hash)

def verify_user(token, email, user_data):
    # verify the user token is a valid google oauth2 token
    request = requests.Request()

    try:
        token_info = id_token.verify_token(
            token, request, GOOGLE_AUDIENCE)
    except ValueError:
        token_info = {'iss': ""}

    verified = True
    # check this has the correct issuer and the emails match
    if token_info['iss'] != "accounts.google.com":
        verified = False

    try:
        if token_info['email'] != email:
            verified = False
        if not user_data.valid_user(token_info['email']):
            verified = False
    except KeyError:
        verified = False

    if verified:
        return token_info['email'], hash_access_token(token), "granted"
    else:
        return "error","error","no"

def process_query(request, schema_query):
    # process the request from the url
    url_hash=request.args.get("hash")
    data_body=request.get_json()
    data_query=data_body["query"]
    data_variables=data_body.get("variables",{})

    # get token
    token_cookie=request.cookies.get(GOOGLE_COOKIE_NAME,"")

    # set project access
    user_data=Data()
    project_access_list = user_data.get_project_access(token_cookie)
    user_data.set_project_access_filters(project_access_list)

    firecloud_schema=graphene.Schema(query=schema_query, auto_camelcase=False)

    result=firecloud_schema.execute(data_query, variables=data_variables, context={"user_data":user_data})
    if result.errors:
        print("ERROR")
        print(data_query)
        print(data_variables)
        print(result.errors)

        # clear the cache
        user_data.cache['expires']={}

    # filter out items that should not be servered without auth
    schema.filter_noauth(result.data,token_cookie,user_data)

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
        user_data=Data()
        return flask.jsonify(user_data.get_version())

    # add static endpoint for access
    @app.route('/access', methods=["POST"])
    def get_access():
        data_body=flask.request.get_json()
        user_data=Data()
        email, hash_token, access = verify_user(data_body["token"],data_body["email"],user_data)
        if access == "granted":
            logging.info("Access GRANTED for user: " + email)
            # adding token to the database
            user_data.add_token(email, hash_token)
            logging.info("Added token to the database for user")
        else:
            logging.info("Access DENIED for user request from email: " + data_body["email"])
        return flask.jsonify({ "hash_token": hash_token })

    # start the app
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
