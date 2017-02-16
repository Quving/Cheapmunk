#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from cheapmunk import *
from lxml import html, cssselect

###################################################################################################################

# Gib eine Liste mit Produkten aus, wie angeboten werden. (Diese Woche)
def getRealAngebote():
	url = "https://www.real.de/markt/wochenangebote-nach-kategorien/lebensmittel"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	products_we = tree.cssselect(".products div[id^=product_]")
	produkte = []
	for product_we in products_we:
		produkt={}

		# Produkt ID
		product_id = product_we.attrib["id"]

		# Produkt Bezeichnung
		produkt["name"] = tree.cssselect("#" + product_id + " div._title")[0].text.encode('utf-8').strip()

		# Produkt Preis
		preis_we = tree.cssselect("#" + product_id + " div.price")[0]
		euro = str(preis_we.text).strip()
		cent = str(preis_we.attrib['data-cents']).strip()
		produkt["preis"] = str(euro) + str(cent)
		# Link zum Produkt
		sub_url = tree.cssselect("#" + product_id + " a")[0].attrib['href']
		produkt["link"] = "http://real.de/" + sub_url

		# Angebotzeitraum
		produkt["datum"] = str(tree.cssselect("small.text-gray")[0].text).strip()	
		produkte.append(produkt)
	return produkte

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
		message += "%s\n\n" % angebot["name"].decode('utf-8')
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