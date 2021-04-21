
# Run this script to add/remove a new user
# Provide the user's email address

# To run: $ python modify_users.py --user test-user@gmail.com

import sys
import argparse

import sqlalchemy

import utilities

def parse_arguments(args):
    """ Parse the arguments from the user """
    parser = argparse.ArgumentParser(
        description= "Add or remove a user from the access lsit\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--user",
        help="user gmail address",
        required=True)
    parser.add_argument(
        "--projects",
        help="one more more projects the user will have access to (comma delimited)",
        required=True)
    parser.add_argument(
        "--function",
        help="function to run",
        choices=["add","remove"],
        default="add")

    return parser.parse_args()

def update_database(engine,command,query=False):
    connection = engine.connect()
    if query:
        results = connection.execute(command)
        for row in results:
            print(row)
    else:
        connection.execute(command)
    connection.close()

def main():

    # get the arguments from the user
    args = parse_arguments(sys.argv)

    # get the database environment variables
    username, password, database = utilities.get_database_variables()

    # create a pool of connections, pre-ping to prevent stale connections
    database_url = "mysql://{username}:{password}@localhost/{database}".format(username = username,
        password = password, database = database)

    try:
        engine = sqlalchemy.create_engine(database_url, pool_size=32, pool_pre_ping=True)
    except EnvironmentError as e:
        print("Unable to connect to local database")
        print("Database url {}".format(database_url))
        sys.exit(e)

    print("Creating users table if not already exists")
    command = "SET sql_notes=0; CREATE TABLE IF NOT EXISTS users(email CHAR(50) PRIMARY KEY, token CHAR(100) DEFAULT 'None', expires CHAR(100) DEFAULT 'None', projects CHAR(100) DEFAULT \"'None'\"); set sql_notes=1;"
    update_database(engine,command)

    if args.function =="add":
        command = "INSERT INTO users (email,projects) VALUES ('{0}',\"{1}\")".format(args.user,",".join(["'"+project+"'" for project in args.projects.split(",")]))
    else:
        command = "DELETE FROM users where email='{}'".format(args.user)

    update_database(engine,command)
    print("Database updated")
    print("Current table")
    update_database(engine,"SELECT * FROM users",query=True)

if __name__ == "__main__":
    main()
