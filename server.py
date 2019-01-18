
# Basic server to host graphql with flask on localhost:5000
# Interfaces to firecloud api

# The initial server was based on the core framework from the example code from
# https://github.com/nderkach/python-grahql-api
# which wraps an end point of the RESTful AirBnB API with GraphQl.
# Code from the example is included in the utilities functions.

import os

import flask
import flask_graphql
import graphene

import schema
import const

NAME = "firecloud_graphql"
HOST = "0.0.0.0"
PORT = "5000"

def process_query(request, schema):
    # process the request from the url
    url_hash=request.args.get("hash")
    data_body_query=request.get_json()['query']

    firecloud_schema=graphene.Schema(query=schema)
    result=firecloud_schema.execute(data_body_query)
    json_result=flask.jsonify(result.data)

    return json_result

def main():
    # create the graphql flask app
    app = flask.Flask(NAME)

    # add the root graphql queries
    @app.route('/graphql', methods=["POST"])
    def get_root_schema():
        json_result = process_query(flask.request, schema.Query)

        # temp use null response (later use json_result)
        return flask.jsonify(const.NULL)

    # add subdirectories to identify schema
    @app.route('/graphql/<name>', methods=["POST"])
    def get_schema(name):
        json_result = process_query(flask.request, schema.Query)

        # temp use const response (later use json_result)
        return flask.jsonify(const.PROJECTS)

    # add static endpoint for version/status
    @app.route('/status', methods=["GET"])
    def get_version():
        return flask.jsonify(const.VERSION)

    # add end point for graphql gui
    app.add_url_rule('/test', view_func=flask_graphql.GraphQLView.as_view(
        'test', schema=graphene.Schema(query=schema.Query), graphiql=True))

    # start the app
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
