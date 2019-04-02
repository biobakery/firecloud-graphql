
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

import schema
import const
from database import data

NAME = "firecloud_graphql"
HOST = "0.0.0.0"
PORT = "5000"

def process_query(request, schema):
    # process the request from the url
    url_hash=request.args.get("hash")
    data_body=request.get_json()
    data_query=data_body["query"]
    data_variables=data_body.get("variables",{})

    firecloud_schema=graphene.Schema(query=schema, auto_camelcase=False)
    result=firecloud_schema.execute(data_query, variables=data_variables)
    if result.errors:
        print("ERROR")
        print(data_query)
        print(data_variables)
        print(result.errors)
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
        return flask.jsonify(data.get_current_version())

    # add end point for graphql gui
    app.add_url_rule('/test', view_func=flask_graphql.GraphQLView.as_view(
        'test', schema=graphene.Schema(query=schema.Query, auto_camelcase=False), graphiql=True))

    # start the app
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
