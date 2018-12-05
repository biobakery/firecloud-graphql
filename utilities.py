
import json
import collections

from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema

# These functions are based on code from
# https://github.com/nderkach/python-grahql-api

def create_graphql_flask_app(name,query):
    """ Create a flask app with graphql schema """

    view_func = GraphQLView.as_view(
        'graphql', schema=Schema(query=query), graphiql=True)
    app = Flask(name)
    app.add_url_rule('/graphql', view_func=view_func)

    return app

def run_app(app, host, port):
    """ Start the flask app on host and port """
    app.run(host=host, port=port)

def _json_object_hook(d):
    return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

