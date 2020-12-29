#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

# TODO: Добавить в бд таблицу с вопросами и забивать от туда по одному
import data_base

import config.token as token_bot

import logging

import data_base

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIRST_Q, SECOND_Q, THREE_Q, FOUR_Q = range(4)

count = 0


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Подобрать автомобиль']]
    user = update.message.from_user

    update.message.reply_text(
        f'Привет {user.first_name}. Помогу тебе подобрать автомобиль,согласно твоим предпочтениям.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return FIRST_Q


def gender(update: Update, context: CallbackContext) -> int:
    global count
    count += 1
    str_question = data_base.get_question(count)
    update.message.reply_text(
        str_question,
        reply_markup=ReplyKeyboardRemove(),
    )
    return SECOND_Q


def pender(update: Update, context: CallbackContext) -> int:
    #logger.info("Gender of %s: %s", user.first_name, update.message.text)
    global count
    count += 1
    str_question = data_base.get_question(count)
    update.message.reply_text(
        str_question,
        reply_markup=ReplyKeyboardRemove(),
    )
    return THREE_Q


def fender(update: Update, context: CallbackContext) -> int:
    #logger.info("Gender of %s: %s", user.first_name, update.message.text)
    global count
    count += 1
    str_question = data_base.get_question(count)
    update.message.reply_text(
        str_question,
        reply_markup=ReplyKeyboardRemove(),
    )

    return FOUR_Q

def blender(update: Update, context: CallbackContext) -> int:
    #logger.info("Gender of %s: %s", user.first_name, update.message.text)
    global count
    count += 1
    str_question = data_base.get_question(count)
    update.message.reply_text(
        str_question,
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END



def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token_bot.token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_Q: [MessageHandler(Filters.text, gender)],
            SECOND_Q: [MessageHandler(Filters.text, pender)],
            THREE_Q: [MessageHandler(Filters.text,fender)],
            FOUR_Q: [MessageHandler(Filters.text,blender)]
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