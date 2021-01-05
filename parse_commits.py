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

def create_commit_list(database, query, text_file):
    conn = create_connection(database)
    c = conn.cursor()

    if conn is not None:
            c.execute(query)
            results = c.fetchall()
            final_result = [i[0] for i in results]
            with open(text_file, 'w') as f:
                for row in final_result:
                    f.write("%s\n" % str(row))
            conn.commit()
            conn.close()

    else:
        print("Error! cannot create the database connection.")

def create_list(database, query, text_file):
    conn = create_connection(database)
    c = conn.cursor()

    if conn is not None:
            c.execute(query)
            results = c.fetchall()
            final_result = [i[0] for i in results]
            with open(text_file, 'w') as f:
                for row in final_result:
                    if row.strip('\n') != 'None':
                        f.write("%s\n" % str(row).split('#'))
            conn.commit()
            conn.close()

    else:
        print("Error! cannot create the database connection.")

def parse_commits(text_file1, text_file2):
    commits_list = []
    with open(text_file1, 'r') as file1:
        with open(text_file2, 'r') as file2: 
            commits = [line.strip() for line in file1]
            lines = [line.strip() for line in file2]
            for commit in commits:
                for line in lines:
                    if str(commit) in line: 
                        commits_list.append(commit)
    #print(count)
    final_list = list(dict.fromkeys(commits_list))
    print(len(final_list))

def main():
    database = r"../sqlite/db/msr_db.db"
    
    gh_commits_query = 'SELECT gh_commits_in_push FROM selected_travis GROUP BY gh_commits_in_push'
    create_list(database, gh_commits_query, 'docs/gh_commits_in_push.txt')

    not_pr_query = 'SELECT fixCommitSha1 FROM (SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE fixCommitSha1 = git_trigger_commit GROUP BY fixCommitSha1) WHERE gh_is_pr = "False"'
    create_commit_list(database, not_pr_query, 'docs/not_a_pr_commit.txt')

    parse_commits('docs/not_a_pr_commit.txt', 'docs/gh_commits_in_push.txt')
    
if __name__ == '__main__':
    main()
