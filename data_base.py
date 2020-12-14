import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('quest_answ.db')
    return __connection


def get_question():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT question FROM questions WHERE id = 1')
    (res,) = c.fetchone()
    return res