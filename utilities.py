
import json
import collections

from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema

from flask import jsonify

# The initial functions were based on code from
# https://github.com/nderkach/python-grahql-api

def create_graphql_flask_app(name,query,version):
    """ Create a flask app with graphql schema """

    # add the graphql queries
    view_func = GraphQLView.as_view(
        'graphql', schema=Schema(query=query), graphiql=True)
    app = Flask(name)
    app.add_url_rule('/graphql', view_func=view_func)

    # add static endpoint for version/status
    def get_version():
        return jsonify(version)
    app.add_url_rule('/status', view_func=get_version)

    return app

def run_app(app, host, port):
    """ Start the flask app on host and port """
    app.run(host=host, port=port)

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

