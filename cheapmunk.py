 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegrambotservice import *
from jobs import *
from usermanagement import *
from realangebote import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters, Job
from telegram import KeyboardButton, ReplyKeyboardMarkup

###################################################################################################################

def start(bot, update):
	setMessageString("Ich suche nach Angeboten! :)")
	sendMessage(bot, update)

	setMessageString(str(getUsers()))
	sendMessage(bot, update)
	
###################################################################################################################

def search_products(name_list):
	angebote_all = getRealAngebote()
	angebote_found = []
	outputmsg = []
	clearMessages()
	for name in name_list:
		for angebot in angebote_all:
			angebot_bezeichung = angebot["name"]

			if name in angebot_bezeichung.lower() and not angebot in angebote_found:
				angebote_found.append(angebot)

	for angebot in angebote_found:
		message = ""
		message += "%s\n\n" % angebot["name"]
		message += "%s\n" % angebot["preis"]
		message += "%s\n\n" % angebot["datum"]
		message += "%s" % angebot["link"]
		outputmsg.append(message)

	# Gebe Nachrichten zurück.
	return outputmsg

###################################################################################################################

def subscribe_products(bot, update, name_list):
	for name in name_list:
		subscribe(update.message.from_user["id"], name)

	# Sende Nachricht
	abos = getSubscribeList(update.message.from_user["id"])
	if abos:
		msg = "Du hast abonniert: \n\n"
		for abo in abos:
			msg+=(" - "+ abo+"\n")

		setMessageString(msg)
	else: 
		setMessageString("Du hast nichts abonniert.")
	sendMessage(bot, update)


###################################################################################################################

def unsubscribe_products(bot, update, name_list):
	for name in name_list:
		unsubscribe(update.message.from_user["id"], name)

	# Sende Nachricht
	abos = getSubscribeList(update.message.from_user["id"])
	if abos:
		msg = "Du hast abonniert: \n\n"
		for abo in abos:
			msg+=(" - "+ abo+"\n")

		setMessageString(msg)
	else: 
		setMessageString("Du hast nichts abonniert.")
	sendMessage(bot, update)


###################################################################################################################

def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


###################################################################################################################

def message_interpreter(bot, update):
	msg_splitted = update.message.text.lower().split(" ")	
	cmd = msg_splitted[0]
	registerUser(update.message.from_user, bot, update)

	if cmd == "search":
		search_list = []
		for to_search in msg_splitted[1:]:
			search_list.append(to_search.encode("utf-8"))
		msglist = search_products(search_list)
		
		if msglist:
			setMessageList(msglist)
		else:
			setMessageString("Gegenwärtig keine Angebote.")
		sendMessage(bot, update)


	if cmd == "subscribe":
		subscribe_list = []
		for to_subscribe in msg_splitted[1:]:
			subscribe_list.append(to_subscribe.encode("utf-8"))
		subscribe_products(bot, update, subscribe_list)


	if cmd == "unsubscribe":
		unsubscribe_list = []
		for to_unsubscribe in msg_splitted[1:]:
			unsubscribe_list.append(to_unsubscribe.encode("utf-8"))
		unsubscribe_products(bot, update, unsubscribe_list)


	if cmd == "source":
		keyboard = [[KeyboardButton("Real!", callback_data='1'),
		             KeyboardButton("Rewe!", callback_data='0')]]

		reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard = True, resize_keyboard = True)
		update.message.reply_text('%i Bitte wähle eine Quelle aus.' % len(messages), reply_markup=reply_markup)


###################################################################################################################

def helpme(bot, update):
	msg = "\"search <produktname>\" - Sucht ein Produkt unter den aktuellen Angeboten.\n\n"
	msg+= "\"subscribe <produktname>\" - Informiere mich jeden Montag, falls das Produkt im Angebot ist.\n\n"
	msg+= "\"unsubscribe <produktname>\" -  Höre auf, mich über das Produkt zu informieren.\n\n"
	msg+= "Ich hoffe, ich war Dir behilflich! :)"
	bot.sendMessage(update.message.chat_id, text=msg)


###################################################################################################################

def main():
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s' +
                    '- %(name)s - %(levelname)s - %(message)s')
	logger = logging.getLogger(__name__)

	# Create the Updater and pass it your bot's token.
	updater = Updater("291218007:AAEKDywDY5B2liyHQzsS480QlqYEbOpPRgE")

	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('readme', helpme))

	updater.dispatcher.add_handler(CallbackQueryHandler(button))
	updater.dispatcher.add_handler(MessageHandler([Filters.text], message_interpreter))
	updater.dispatcher.add_error_handler(error)

	jobqueue = updater.job_queue

	# User datebase:	
	loadusers()

	# Job: 13 Stunden Takt.
	job_hour = Job(callback_hour, 46800)
	jobqueue.put(job_hour, next_t=0.0)


	# Start the Bot
	updater.start_polling()


	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()

# start Main Methode.
if __name__ == '__main__':
    main()
