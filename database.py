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
    
    # JSON files
    sstubs = 'docs/json-data/sstubs.json'
    selected_travis = 'docs/json-data/selected_travis.json'
    selected_sstubs = 'docs/json-data/selected_sstubs.json'

    # CSV files
    apache_flink = 'docs/commit-guru/apache-flink.csv'
    apache_storm = 'docs/commit-guru/apache-storm.csv'
    checkstyle = 'docs/commit-guru/checkstyle.csv'
    closure_compiler = 'docs/commit-guru/closure-compiler.csv'
    dropwizard_dropwizard = 'docs/commit-guru/dropwizard-dropwizard.csv'
    dropwizard_metrics = 'docs/commit-guru/dropwizard-metrics.csv'
    druid = 'docs/commit-guru/druid.csv'
    google_guice = 'docs/commit-guru/google-guice.csv'
    graylog2 = 'docs/commit-guru/graylog2.csv'
    jedis = 'docs/commit-guru/jedis.csv'
    junit = 'docs/commit-guru/junit-team-junit.csv'
    mybatis = 'docs/commit-guru/mybatis-mybatis-3.csv'
    naver = 'docs/commit-guru/naver-pinpoint.csv'
    presto = 'docs/commit-guru/presto.csv'

    # Commits from the original Sstubs dataset 
    create_table(sstubs, database, 'sstubs')

    # Travis Torrent builds for projects selected in Sstubs
    create_table(selected_travis, database, 'selected_travis')

    # Sstubs Commits from selected projects
    create_table(selected_sstubs, database, 'selected_sstubs')

    # Commit Guru Table
    create_commit_guru_table(apache_flink, database)
    create_commit_guru_table(apache_storm, database)
    create_commit_guru_table(checkstyle, database)
    create_commit_guru_table(closure_compiler, database)
    create_commit_guru_table(dropwizard_dropwizard, database)
    create_commit_guru_table(dropwizard_metrics, database)
    create_commit_guru_table(druid, database)
    create_commit_guru_table(google_guice, database)
    create_commit_guru_table(graylog2, database)
    create_commit_guru_table(jedis, database)
    create_commit_guru_table(mybatis, database)
    create_commit_guru_table(naver, database)
    create_commit_guru_table(presto, database)
    create_commit_guru_table(junit, database)

if __name__ == '__main__':
    main()