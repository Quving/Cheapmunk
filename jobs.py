#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from cheapmunk import search_products
from telegrambotservice import setMessageList, sendMessageTo
from usermanagement import getUsers

def callback_hour(bot, job):
	# Wenn Montag
	if time.strftime("%w") == 1:
		output = {}
		users = getUsers()

		for user_id_str in users.keys():
			output[user_id_str] = []
			for prod in users[user_id_str]["subscribe_list"]:
				output[user_id_str]+=search_products([prod])

		for user_id_str in output.keys():
			if output[user_id_str]:
				setMessageList(output[user_id_str])
				sendMessageTo(bot, int(user_id_str))
