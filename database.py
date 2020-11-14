import sqlite3
from sqlite3 import Error

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"../sqlite/db/sstubs.db"

    sql_create_commits_table = """ CREATE TABLE IF NOT EXISTS commits (
                                        id integer PRIMARY KEY,
                                        bug_type text NOT NULL, 
                                        fix_commit_sha1 text NOT NULL,
                                        fix_commit_parent_sha1 text NOT NULL, 
                                        bug_file_path text,
                                        fix_patch text, 
                                        project_name text,
                                        bug_line_number integer, 
                                        bug_node_start_char integer, 
                                        bug_node_length integer, 
                                        fix_line_number integer, 
                                        fix_node_start_char integer, 
                                        fix_node_length integer, 
                                        source_before_fix text, 
                                        source_after_fix text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_commits_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()