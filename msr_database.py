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

def create_sstubs_commits_table(selected_sstubs, database):
    with open(selected_sstubs) as json_file:
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

        sql_create_travis_table = "create table if not exists sstubs_commits ({0})".format(" text,".join(columns))

        sql_insert_travis = "insert into sstubs_commits ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        # create a database connection
        conn = create_connection(database)
        c = conn.cursor()
        # create tables
        if conn is not None:
            c.execute(sql_create_travis_table)
            c.executemany(sql_insert_travis, values)
            values.clear()
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

def create_travis_torrent_table(merged_travis, database):
    with open(merged_travis) as json_file:
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

        sql_create_travis_table = "create table if not exists travis_builds ({0})".format(" text,".join(columns))

        sql_insert_travis = "insert into travis_builds ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        # create a database connection
        conn = create_connection(database)
        c = conn.cursor()
        # create tables
        if conn is not None:
            c.execute(sql_create_travis_table)
            c.executemany(sql_insert_travis, values)
            values.clear()
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

def main():
    database = r"../sqlite/db/msr_db.db"
    travis_file = 'docs/selected_merged_travis.json'
    sstubs_file = 'docs/selected_sstubs_projects.json'
    create_sstubs_commits_table(sstubs_file, database)
    create_travis_torrent_table(travis_file, database)

if __name__ == '__main__':
    main()

