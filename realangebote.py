#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
from lxml import html, cssselect


# Gib eine Liste mit Produkten aus, wie angeboten werden. (Diese Woche)
def getRealAngebote():
	url = "http://prospekt.real.de/wochenangebote-nach-kategorien/alle-angebote.html"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	angebote = tree.cssselect("a.product_name")
	preise = tree.cssselect("div.preismarke_small.clearfix")
	datum = tree.cssselect("span.tc_bright_grey.fs_15")[0].text

	angebote_output = []
	produkte=[]
	for angebot, preis in zip(angebote, preise):
		produkt={}
		produkt["name"] = angebot.text
		produkt["preis"] = preis.attrib["title"]
		produkt["link"] = "http://prospekt.real.de/"+ angebot.attrib["href"]
		produkt["datum"] = datum[11:]
		produkte.append(produkt)
	return produkte




def getReweAngebot():
	url = "https://www.rewe.de/angebote/"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	angebote = tree.cssselect(".dotdot div")
	preise = tree.cssselect("div.pricebox div.price")
	preise_kl = tree.cssselect("div.pricebox div.price small")
	link_id = tree.cssselect("h2.controller.title")	
	#datum = tree.cssselect("div.drop")[0].text + " " + tree.cssselect("div.drop span.days")[0].text



	#datum = tree.cssselect("span.tc_bright_grey.fs_15")[0].text

	angebote_output = []
	produkte=[]
	for angebot, preis, preis_kl, link in zip(angebote, preise, preise_kl,link_id):
		produkt={}
		produkt["name"] = angebot.text
		produkt["preis"] = preis.text + preis_kl.text
		produkt["link"] = "https://www.rewe.de/angebote/?show="+ link.attrib["data-query"]
		#produkt["datum"] = datum
		produkte.append(produkt)
	return produkte





