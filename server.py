
# Basic server to host graphql with flask on localhost:5000
# Interfaces to firecloud api

# The initial server was generated using the example code from
# the REST wrapper from graphql example at https://github.com/nderkach/python-grahql-api

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
