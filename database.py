import sqlite3
from sqlite3 import Error
import json
import pandas as pd 

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

def create_table(file_in, database, table_name):
    with open(file_in) as json_file:
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

        sql_create_table = "create table if not exists " + table_name + " ({0})".format(" text,".join(columns))

        sql_insert = "insert into " + table_name + " ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        # create a database connection
        conn = create_connection(database)
        c = conn.cursor()
        # create tables
        if conn is not None:
            c.execute(sql_create_table)
            c.executemany(sql_insert, values)
            values.clear()
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

def create_commit_guru_table(commit_guru_file, database):
    commits = pd.read_csv(commit_guru_file)
    conn = create_connection(database)

    commits.to_sql('commit_guru', conn, if_exists = 'append', index = False)
    conn.commit()
    conn.close()

def main():
    database = r"../sqlite/db/msr_challenge.db"
    sstubs = 'docs/json-data/sstubs.json'
    selected_travis = 'docs/json-data/selected_travis.json'
    selected_sstubs = 'docs/json-data/selected_sstubs.json'

    # Commits from the original Sstubs dataset 
    create_table(sstubs, database, 'sstubs')

    # Travis Torrent builds for projects selected in Sstubs
    create_table(selected_travis, database, 'selected_travis')

    # Sstubs Commits from selected projects
    create_table(selected_sstubs, database, 'selected_sstubss')

    # Project in CommitGuru

if __name__ == '__main__':
    main()