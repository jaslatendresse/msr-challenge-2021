import sqlite3
from sqlite3 import Error

# Query selected_travis to select 'gh_commits_in_push' 
# Parse the results: can either have 'None' or a list of commits separated by '#'
# Split the string on '#' where the entry is not 'None' --> can use split('#')
# Store in some datastructure 
# Query selected_sstubs to check how many commits are in the list we just created 

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

def create_list(database, table_name, column_name):
    query = 'SELECT ' + column_name + ' FROM ' + table_name

    conn = create_connection(database)
    c = conn.cursor()

    if conn is not None:
            c.execute(query)
            results = c.fetchall()
            final_result = [i[0] for i in results]
            with open('docs/gh_commits_in_push.txt', 'w') as f:
                for row in final_result:
                    if row.strip('\n') != 'None':
                        f.write("%s\n" % str(row))
            conn.commit()
            conn.close()

    else:
        print("Error! cannot create the database connection.")

#def parse_list(text_file):


def main():
    database = r"../sqlite/db/msr_db.db"
    create_list(database, 'selected_travis', 'gh_commits_in_push')

if __name__ == '__main__':
    main()
