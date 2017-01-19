#!/usr/bin/python*
# -*- coding: utf-8 -*-

import requests
from lxml import html, cssselect


def updateSaleList():
	foo = "bar"


def getSteamSales():
	url="https://steamdb.info/sales/"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	spielenames = tree.cssselect("tr.app.appimg a[href^='/app/'].b")
	
	with open("current_in_sale.txt", "w") as file:
		for spieltitel in spielenames:
			file.write(spieltitel.text.encode("utf-8"))

	prices = []
	for idx2, spiel in enumerate(spielenames):
		print("Spielnummer: "+ str(idx2))
		url = "https://steamdb.info/"+spiel.attrib["href"]
		page_spiel = requests.get(url)
		tree_page = html.fromstring(page_spiel.content)
		rows = tree_page.cssselect("td.price-line")
		index = -1
		for idx, val in enumerate(rows):
			data_cc = val.attrib["data-cc"]
			if data_cc == "eu":
				index = idx
				break;

		if index == -1:
			price = "N/A at"
		else:
			if index < len(tree_page.cssselect("td[data-sort='0']")):
				price = tree_page.cssselect("td[data-sort='0']")[idx].text
			else:
				price = "N/A at"
		prices.append(price)

		break
		

	spielerabatt = tree.cssselect("td.price-discount")
	

	with open("steamdb.html", "w") as file:
		file.write(page.content)

	with open("spieleliste.txt", "w") as file:
		for spielname, price in zip(spielenames, prices):
			file.write(spielname.text.encode("utf-8")+"\t"+ price.encode("utf-8").split(" ")[0]+"\n")
	dic = {}
	for spielname, price in zip(spielenames, prices):
		dic[spielname.text.encode("utf-8")] =  price.encode("utf-8").split(" ")

	return dic		


def main():
	getSteamSales()

if __name__ == '__main__':
    main()

