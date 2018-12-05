
# Basic server to host graphql with flask on localhost:5000
# Interfaces to firecloud api

# The initial server was based on the core framework from the example code from
# https://github.com/nderkach/python-grahql-api
# which wraps an end point of the RESTful AirBnB API with GraphQl.
# Code from the example is included in the utilities functions.

import os

import schema
import utilities

HOST = "0.0.0.0"
PORT = "5000"

def main():
    app=utilities.create_graphql_flask_app("firecloud_graphql", schema.Query)
    utilities.run_app(app, HOST, PORT)

if __name__ == '__main__':
    main()
