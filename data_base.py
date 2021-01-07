#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

import sqlite3
import csv

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
        c.execute('DROP TABLE IF EXISTS Quest')
        c.execute('DROP TABLE IF EXISTS Answer')
        c.execute('DROP TABLE IF EXISTS QuestRules')

    with open('database_config/quest.txt', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        print(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                c.execute('''
                    CREATE TABLE IF NOT EXISTS Quest(
                        id_quest      INTEGER PRIMARY KEY,
                        question   TEXT NOT NULL,
                        answer1 TEXT,
                        answer2 TEXT,
                        answer3 TEXT,
                        answer4 TEXT
                    )
                ''')
                line_count += 1
            else:
                print(row[1])
                c.execute('INSERT INTO Quest VALUES (?,?,?,?,?,?)', (row[0], row[1], row[2], row[3], row[4], row[5]))
                line_count += 1

    c.execute('''
        CREATE TABLE IF NOT EXISTS Answer(
            id_answer      INTEGER PRIMARY KEY,
            id_telegram   INTEGER NOT NULL,
            answer1 TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS QuestRules(
            id_qr      INTEGER PRIMARY KEY,
            if_par   INTEGER NOT NULL,
            then_value TEXT NOT NULL,
            next_quest INTEGER NOT NULL 
        )
    ''')

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
