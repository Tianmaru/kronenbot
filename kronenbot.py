#!/usr/bin/python
# -*- coding: utf8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from datetime import time
import logging
import os
import argparse

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MOIN = 'Einen wunderschönen guten Moin! Es ist dreiviertel neun, ich trinke meinen Kaffee am liebsten mit Milch und Zucker!'
FOOGAKBAZ_ID = 0
TELEGRAM_TOKEN = ""

argparser = argparse.ArgumentParser()
argparser.add_argument("-t", "--telegramtoken", type=str)
argparser.add_argument("-f", "--foogakbaz", type=int)
args = argparser.parse_args()

# Get telegram token
if args.telegramtoken:
    TELEGRAM_TOKEN = args.telegramtoken
if TELEGRAM_TOKEN == "":
    if "RUVEN_BOT_TG_TOKEN" in os.environ:
        TELEGRAM_TOKEN = os.environ["RUVEN_BOT_TG_TOKEN"]
    else:
        logger.error(
            "Telegram Token not provided. Ensure that your bot token is stored in RUVEN_BOT_TG_TOKEN"
            " or supplied as an argument.")
        exit(-1)

if args.foogakbaz:
    FOOGAKBAZ_ID = args.foogakbaz
elif "RUVEN_BOT_GROUP_ID" in os.environ:
    FOOGAKBAZ_ID = os.environ["RUVEN_BOT_GROUP_ID"]
else:
    logger.error("Foogakbaz id not provided.")
    exit(-1)


def callback_moin(context):
    context.bot.send_message(chat_id=FOOGAKBAZ_ID, text=MOIN)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    logger.info('Starting the bot...')
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.job_queue.run_daily(callback_moin, time(hour=8, minute=45), name='moin')

    # log all errors
    logger.info('Adding error handler...')
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    logger.info('Start polling...')
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logger.info('Go into idle mode...')
    updater.idle()


if __name__ == '__main__':
    main()
