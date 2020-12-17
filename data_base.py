import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('questions.db')
    return __connection


def get_question(id_quest: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT question FROM main_questions WHERE id =? ', (id_quest,))
    (res,) = c.fetchone()
    return res


def get_answers(id_quest: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT answer_1,answer_2,answer_3,answer_4 FROM main_questions WHERE id =?', (id_quest,))
    (res,) = c.fetchall()
    return res


