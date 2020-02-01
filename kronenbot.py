#!/usr/bin/python
# -*- coding: utf8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from pytz import timezone
import datetime
import logging
import os
import argparse
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MOIN = "Einen wunderschönen guten Moin! Es ist dreiviertel neun, ich trinke meinen Kaffee am liebsten mit Milch und " \
       "Zucker!"
TIME = timezone('CET').localize(
    datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour=8, minute=45))).astimezone().time()
LIFEHACK_TEMPLATE = "Und hier der Kaffee-Lifehack des Tages: *{}*\n\n{}"
LIFEHACKS = [
    ("Body-Scrub: Kaffee-Körperpeeling", "Mit Kaffeesatz kann die eigene Haut verwöhnt werden. Für das "
                                         "Body-Scrub-Kaffee-Peeling benötigt man lediglich einen Esslöffel Kokosöl ("
                                         "in Drogerien erhältlich) und einen Esslöffel Kaffeesatz. Gut vermischen "
                                         "lassen sich diese zwei Zutaten in einer kleinen Schale – mit dem Gemisch "
                                         "dann ein- bis zweimal pro Woche die Haut zu massieren. Dadurch wird sie auf "
                                         "Dauer weich und gepflegt. Außerdem unterstützt das Koffein die Straffung "
                                         "der Haut."),
    ("Kühlschrankgeruch adé", "Es stehen geruchsintensive Lebensmittel im Kühlschrank und der Geruch kommt einem jedes "
                              "Mal entgegen sobald die Kühlschranktür geöffnet wird. Die Lösung: Einfach ein kleines "
                              "Gefäß mit Kaffeesatz über Nacht im Kühlschrank platzieren. Schon sind die unangenehmen "
                              "Gerüche verschwunden."),
    ("Mülleimergeruch neutralisieren", "Unschöne Gerüche können ebenfalls im Mülleimer entstehen. Daher leistet auch "
                                       "hier der Kaffee Abhilfe. Den Abfall mit Kaffeesatz überstreuen und nach kurzer "
                                       "Zeit ist der Müllgeruch verflogen."),
    ("Gerüche aus Gefäßen entfernen", "Durch verschiedene Lebensmittel wie Käse, Knoblauch oder Zwiebeln bleiben "
                                      "Gerüche an Gefäßen wie Schraubgläsern oder Plastikbehältern haften. Loswerden "
                                      "kann man sie, indem Kaffeesatz über ein paar Tage verschlossen in den Gefäßen "
                                      "aufbewahrt wird."),
    ("Gewächse düngen", "Auch für das Düngen von Pflanzen kann man Kaffeesatz verwenden: Indem die Erde damit "
                        "vermischt wird, reichert man sie mit zusätzlichen Nährstoffen an. Diese Art von Dünger "
                        "eignet sich außerdem bei Einpflanzungen."),
    ("Ameisen vertreiben", "Damit die kleinen Tierchen den Beeten fernbleiben, Kaffeesatz in Form eines Walles "
                           "drumherum verteilen. Der neutralisierende Kaffee lässt die von Ameisen gelegten "
                           "Duftspuren verschwinden. Somit wird man die Störenfriede ohne ein Giftmittel los."),
    ("Geruchsblindheit nach Parfümtests bekämpfen", "Auf der Suche nach dem passenden Parfüm aus der eigenen Sammlung "
                                                    "kann es schon mal zur Geruchsblindheit kommen. Damit man auch "
                                                    "nach einigen Parfümtests weiterschnuppern kann, hilft es, "
                                                    "am Kaffeesatz oder an Kaffeebohnen zu riechen. Danach lassen "
                                                    "sich Gerüche direkt wieder wahrnehmen."),
    ("Backen mit Kaffee", "Aufgegossener Kaffee eignet sich gut als Zutat, um Gebäcken wie Keksen oder Kuchen eine "
                          "besondere Note zu verleihen. Besonders beliebt unter Kaffeegebäcken ist der "
                          "Kaffee-Gugelhupf."),
    ("Grill reinigen", "Gegrilltes hinterlässt meist Spuren auf dem Grillrost, die sich nur schwer beseitigen lassen. "
                       "Für die umweltbewusste Säuberung nach dem Einweichen des Rosts anstelle von Scheuermilch "
                       "Kaffeesatz auf den Schwamm geben. Dieser hat den gleichen Effekt wie Scheuermilch."),
    ("Färben mit Kaffee", "Über versehentlich verschütteten Kaffee wird sich oft geärgert, denn er hinterlässt stark "
                          "sichtbare Flecken. Doch diese eher ungewünschte Eigenschaft hat auch Vorteile: Den "
                          "Kaffesatz im lauwarmen Wasser auflösen und beispielweise für das Färben von Stoffen, "
                          "Ostereiern und Bastelpapier verwenden. Auch Kratzer in Holzmöbeln können mithilfe von "
                          "Kaffee abgedeckt werden. Dafür den Kaffeesatz leicht befeuchten und vorsichtig auf die "
                          "Kratzer auftragen."),
    ("5 Kaffee-Lifehacks (Video)", "https://www.youtube.com/watch?v=u4lnjKviYyk"),
    ("Haustierpflege",
     "Vergessen Sie teure Mittel für die Pflege Ihrer Liebsten! Haben Hunde oder Katzen Flöhe, greifen Sie zum "
     "Wundermittel Kaffee! Für den Hund empfiehlt sich dabei das Vermischen des Satzes mit Shampoo oder nur mit "
     "Wasser. Dann Baden Sie Ihren treuen Freund ausgiebig damit und Sie werden sehen, der Hund ist und bleibt "
     "Floh-Frei. Katzenliebhaber aufgepasst! Stellen Sie ein Glas Zitronensaft (oder andere Zitrusfrucht) vermischt "
     "mit Kaffeesatz an die Orte, an denen sich ihr Stubentiger nach draußen und drinnen bewegt. Ungebetene Gäste im "
     "Katzenfell werden bei dem starken Zitrus- und Kaffeegeruch gleich das Weite suchen."),
    ("Holzböden reparieren",
     "Immer wenn Sie an diesem hässlichen Kratzer in Ihrem Parkett vorbeigehen ärgern Sie sich grün und blau? Hier "
     "kommt Abhilfe! Mischen Sie etwas warmes Wasser mit Kaffeesatz  und tragen es auf die Kratzer in Ihrem Holzboden "
     "auf. Einwirken lassen, fertig! Kaffee wirkt als natürliches Färbemittel und kann nach einer kurzen Einwirkzeit "
     "wieder entfernt werden."),
    ("Trinken",
     "Eine fromme Legende besagt, dass der islamische Prophet Mohammed die anregende Wirkung des Kaffees zuerst "
     "entdeckt habe, nachdem ihm der Engel Gabriel eine Tasse heißer, dunkler Flüssigkeit dargeboten habe. Diese "
     "verschwenderische Verwendung von Kaffee sollte aber nur im äußersten Notfall angewendet werden - kurz bevor er "
     "schlecht wird.")
]
NAME_TEMPLATE = "Mein heutiger Name ist *{} {}{}*."
FIRST_NAME = ["Ruven", "Ruben", "Luven", "Risto", "Ruru"]
LAST_NAME_1 = ["Kronen", "Kanonen", "Klonen", "Kloster", "Kamem", "Pylonen", "Dämonen"]
LAST_NAME_2 = ["berg", "bert", "gert", "burg", "bart", "zerg"]

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
    (lifehack_title, lifehack_text) = random.choice(LIFEHACKS)

    message = MOIN + "\n\n"
    message += NAME_TEMPLATE.format(FIRST_NAME, LAST_NAME_1, LAST_NAME_2) + "\n\n"
    message += LIFEHACK_TEMPLATE.format(lifehack_title, lifehack_text)
    context.bot.send_message(chat_id=FOOGAKBAZ_ID, text=message, parse_mode="Markdown")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    logger.info('Starting the bot...')
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.job_queue.run_daily(callback_moin, TIME, name='moin')

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
