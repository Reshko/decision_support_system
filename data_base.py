import sqlite3
import json

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('questions.db')
    return __connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS questions')

    c.execute('''
        CREATE TABLE IF NOT EXISTS questions(
            id      INTEGER PRIMARY KEY,
            question   TEXT NOT NULL,
            answer_1 TEXT,
            answer_2 TEXT,
            answer_3 TEXT,
            parametr TEXT
        )
    ''')


    # TODO Сделать автоматическое вливание вопросов
    # Вливание данных из файла в бд
    #for i in _group:
        #c.execute('INSERT INTO all_group (numberGroup) VALUES (?)', (i,))

    # Сохранение изменений
    conn.commit()

def get_question(id_quest: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT question FROM questions WHERE id =? ', (id_quest,))
    (res,) = c.fetchone()
    return res


def get_answers(id_quest: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT answer_1,answer_2,answer_3 FROM questions WHERE id =?', (id_quest,))
    (res,) = c.fetchall()
    return res

if __name__ == '__main__':
    init_db(force=True)


