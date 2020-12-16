import sqlite3
from sqlite3 import Error
import json


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_commits_table(commits_json, database):
    with open(commits_json) as json_file:
        json_data = json.loads(json_file.read())

        columns = []
        column = []
        for data in json_data:
                column = list(data.keys())
                for col in column:
                    if col not in columns:
                        columns.append(col)

        value = []
        values = []
        for data in json_data:
                for i in columns:
                    value.append(str(dict(data).get(i)))
                values.append(list(value))
                value.clear()

        sql_create_commits_table = "create table if not exists commits ({0})".format(" text,".join(columns))

        sql_insert_commits = "insert into commits ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        # create a database connection
        conn = create_connection(database)
        c = conn.cursor()
        # create tables
        if conn is not None:
            c.execute(sql_create_commits_table)
            c.executemany(sql_insert_commits, values)
            values.clear()
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

def create_travistorrent_names_table(names_json, database):
    with open(names_json) as json_file:
        json_data = json.loads(json_file.read())

        columns = []
        column = []
        for data in json_data:
                column = list(data.keys())
                for col in column:
                    if col not in columns:
                        columns.append(col)

        value = []
        values = []
        for data in json_data:
                for i in columns:
                    value.append(str(dict(data).get(i)))
                values.append(list(value))
                value.clear()

        sql_create_names_table = "create table if not exists names ({0})".format(" text,".join(columns))

        sql_insert_names = "insert into names ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        # create a database connection
        conn = create_connection(database)
        c = conn.cursor()
        # create tables
        if conn is not None:
            c.execute(sql_create_names_table)
            c.executemany(sql_insert_names, values)
            values.clear()
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

def main():
    database = r"../sqlite/db/sstubs.db"
    commits_file = 'docs/sstubs.json'
    names_file = 'docs/travistorrent_project_names.json'
    travis_file = 'docs/selected_merged_travis.json'
    create_commits_table(commits_file, database)
    create_travistorrent_names_table(names_file, database)

if __name__ == '__main__':
    main()
