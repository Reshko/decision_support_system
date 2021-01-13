#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import data_base as db

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            logger.info(f"Обращение в функцию {f.__name__}")
            return f(*args, **kwargs)
        except Exception:
            logger.exception(f"Ошибка в обработчике {f.__name__}")
            raise

    return inner


FIRST_QUESTION, QUESTIONS = range(2)
number_quest = 0


@debug_requests
def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    logger.info("Start bot")
    reply_keyboard = [['Подобрать автомобиль']]
    user = update.message.from_user
    update.message.reply_text(
        f'Привет {user.first_name}. Помогу тебе подобрать автомобиль,согласно твоим предпочтениям.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return FIRST_QUESTION


@debug_requests
def first_question(update: Update, context: CallbackContext) -> int:
    global number_quest
    number_quest, quest, answers = info_about_quest()
    update.message.reply_text(
        quest,
        reply_markup=ReplyKeyboardMarkup([answers], one_time_keyboard=True, resize_keyboard=True),
    )
    return QUESTIONS


# TODO Заполнить таблицу QuestRules
# TODO Реализовать хранением ответов пользователя UDP:Таблица с колонками вопросов
#  || создать объект user_id {question:answer ... }
# TODO глобальные переменные
@debug_requests
def questions(update: Update, context: CallbackContext) -> int:
    user_answer = update.message.text
    user_id = update.message.chat.id
    global number_quest
    #db.update_date(user_id, user_answer)
    number_next_question = db.quest_rules(user_answer, number_quest)
    new_number_quest, quest, answers = info_about_quest(
        id_quest=number_next_question)  # Передаем полученный ранее номер следующего вопроса
    update.message.reply_text(
        quest,
        reply_markup=ReplyKeyboardMarkup([answers], one_time_keyboard=True, resize_keyboard=True),
    )
    number_quest = new_number_quest
    return QUESTIONS


@debug_requests
def cancel():
    pass


@debug_requests
def info_about_quest(id_quest: int = 12):
    list_quest_answ = [x for x in db.get_quest_info(id_quest) if x]
    number_quest = list_quest_answ[0]
    quest = list_quest_answ[1]
    answ = list_quest_answ[2::]
    logger.info(f'Вопрос {quest}')
    logger.info(f'Ответы {answ}')
    return number_quest, quest, answ


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1433478214:AAHUY3C3tYgOwOK7Ilw6lJzPDbX55y2M9eA", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_QUESTION: [MessageHandler(Filters.text, first_question)],
            QUESTIONS: [MessageHandler(Filters.text, questions)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
