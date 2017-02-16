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
		produkt["name"] = tree.cssselect("#" + product_id + " div._title")[0].text	

		# Produkt Preis
		preis_we = tree.cssselect("#" + product_id + " div.price")[0]
		produkt["preis"] = preis_we.text.strip() + str(preis_we.attrib['data-cents']).strip()

		# Link zum Produkt
		sub_url = tree.cssselect("#" + product_id + " a")[0].attrib['href']
		produkt["link"] = "http://real.de/" + sub_url

		# Angebotzeitraum
		produkt["datum"] = tree.cssselect("small.text-gray")[0].text 				
		produkte.append(produkt)
	return produkte

###################################################################################################################

