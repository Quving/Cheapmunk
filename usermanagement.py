#!/usr/bin/python*
# -*- coding: utf-8 -*-

import json

users = {}

def getUsers():
	global users
	return users
	
def loadusers():
	global users
	try:
		file = open("user.json", "r")
		data = json.load(file)
		file.close()
		users = data
	except IOError:
		file = open("user.json", "w")
		json.dump({}, file, sort_keys=True, indent=4)
		file.close()
		users = {}

def getSubscribeList(user_id):
	global users
	return users[str(user_id)]["subscribe_list"]


def saveusers():
	global users
	with open("user.json", "w") as file:
		json.dump(users, file, sort_keys=True, indent=4)
		file.close()

def subscribe(user_id, subscribe):
	global users
	loadusers()

	if not subscribe in users[str(user_id)]["subscribe_list"]:
		users[str(user_id)]["subscribe_list"].append(subscribe) 
		saveusers()


def unsubscribe(user_id, unsubscribe):
	global users
	loadusers()

	if  unsubscribe in users[str(user_id)]["subscribe_list"]:
		users[str(user_id)]["subscribe_list"].remove(unsubscribe) 
		saveusers()

def registerUser(user, bot, update):
	global users
	loadusers()
	if not str(user["id"]) in users.keys():
		bot.sendMessage(user["id"], "Neuer User.")
		bot.sendMessage(user["id"], str(users.keys()))


		user_dict = {}
		user_dict["first_name"] = user["first_name"]
		user_dict["last_name"] = user["last_name"]
		user_dict["username"] = user["username"]
		user_dict["source_list"] = []
		user_dict["id"] = user["id"]
		user_dict["subscribe_list"] = []
		users[user["id"]] = user_dict
		saveusers()
