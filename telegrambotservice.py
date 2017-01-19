#!/usr/bin/python*
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

messages = []

# Fügt eine weitere Nachricht in die Nachrichten Queue hinzu.,
def appendMessage(message):
	global messages		
	messages.append(message)

# Lösche alle Nachrichten, die aktuell in der Queue sind.
def clearMessages():
	global messages	
	messages = []

# Setze eine neue Nachricht
def setMessageString(message):
	global messages	
	messages = [message]

# Setze eine neue Nachricht
def setMessageList(messageList):
	global messages	
	messages = messageList

# Versende eine Nachricht und benachrichtige den User, falls die Nachrichtenanzahl 10 überschreiten.
def sendMessage(bot, update):
	global messages	
	if len(messages) > 10:
		keyboard = [[InlineKeyboardButton("Yup!", callback_data='1'),
		             InlineKeyboardButton("Nope!", callback_data='0')]]

		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text('%i Resultate anzeigen?' % len(messages), reply_markup=reply_markup)
	else:
		for message in messages:
		    bot.sendMessage(update.message.chat_id, message)

def sendMessageTo(bot, chat_id):
	global messages
	for message in messages:
		    bot.sendMessage(chat_id, message)

def button(bot, update):
	query = update.callback_query
	answer = query.data


	bot.editMessageText(text= query.message.text,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
	bot.sendMessage(query.message.chat_id," message")

	if answer == "1":
		for message in messages:
		    bot.sendMessage(query.message.chat_id, message)


