from http.client import UnimplementedFileMode
import sqlite3
from sqlite3 import Error
import datetime


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(r"db\\pythonsqlite.db")
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

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

def _query(conn, qry):
    try:
        c = conn.cursor()
        c.execute(qry)
        res = c.fetchall()
        print(qry, res)
        return res
    except Error as e:
        print(e)

def get_treaterboard(conn):
    qry = """
        SELECT id, num_treats,last_treat
        from treats
        where id <> '375863038755995648'
        order by num_treats desc
    """
    return _query(conn, qry)

def get_treats(conn, id):
    qry = """
        SELECT id, num_treats, last_treat, date()
        FROM treats
        WHERE id = {}
    """.format(id)
    res = _query(conn, qry)
    message = ''
    if (len(res) == 0):
        _create_treats_user(conn, id)
        treats = 0
    else:
        treats = res[0][1]
        if res[0][2] == res[0][3]:
            message = 'You have already given me a treat today! Don\'t make me fatter than I already am!'
    return message, treats
    # return res

def update_treats(conn, id, treats):
    qry = """
        UPDATE TREATS
        SET 
            num_treats = {},
            last_treat = date()
        WHERE id = {}
    """.format(treats, id)
    _query(conn, qry)

def _create_treats_user(conn, id):
    qry = """
        INSERT INTO treats
        (id, num_treats, last_treat)
        VALUES
        ({}, 0, date())
    """.format(id)
    _query(conn, qry)

def _create_user(conn, id):
    qry = """
        INSERT INTO users (
            id
        ) VALUES
        ({})
    """.format(id)
    _query(conn, qry)

def get_user(conn, id):
    qry = """
        SELECT *
        FROM treats
        WHERE id = {}
    """.format(id)
    res = _query(conn, qry)
    if len(res) == 0:
        _create_user(conn, id)

# def create_user(conn, id):

def drop_table(conn, table):
    qry = """
        drop table {}
    """.format(table)
    c = conn.cursor()
    c.execute(qry)


if __name__ == '__main__':
    db = r"db\\pythonsqlite.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS treats (
                                    id integer PRIMARY KEY,
                                    num_treats integer NOT NULL,
                                    last_treat text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection()
    # drop_table(conn, 'users')
    # drop_table(conn, 'treats')

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")