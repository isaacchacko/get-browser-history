# todo: make it pull history once, more efficient

import browserhistory as bh
from datetime import datetime
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess, Process
import requests
import json
import time 

def shorten(link):
	
	linkRequest = {"destination": link}

	requestHeaders = {
		"Content-type": "application/json",
		"apikey": "c2c1028fec614106bbf42fd5e1d12bff"
	}

	r = requests.post("https://api.rebrandly.com/v1/links", 
		data = json.dumps(linkRequest),
		headers=requestHeaders)

	content = json.loads(r.content)
	link = content['shortUrl']
	link_id = content['id']
	return link, link_id

def delete(id):
	requestHeaders = {
		"Content-type": "application/json",
		"apikey": "c2c1028fec614106bbf42fd5e1d12bff"
	}
	r = requests.delete(f'https://api.rebrandly.com/v1/links/{id}', headers =requestHeaders)

def kChrome(): # function stolen from https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
	listOfProcessObjects = []
	
	for proc in process_iter():
	   try:
		   pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
		   
		   if 'chrome' in pinfo['name'].lower() :
			   listOfProcessObjects.append(pinfo)

	   except (NoSuchProcess, AccessDenied , ZombieProcess) :
		   pass

	for process in listOfProcessObjects:
		p = Process(process['pid'])
		p.terminate()

class History():
	def __init__(self):
		self.browser_history = []
		self.browser_entry = ()

	def close(self):
		if self.browser_history != []:
			for i in self.browser_history:
				delete(i[-1])
		if self.browser_entry != ():
			delete(self.browser_entry[-1])

	def getAll(self, browser, max_index = 100):
		tmp_all_history = bh.get_browserhistory()
		self.browser_history = tmp_all_history[browser][0:max_index]

		for index, i in enumerate(self.browser_history):
			website_url, website_title, date_string = i
			date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
			short_url, lId = shorten(website_url)
			self.browser_history[index] = (website_url, website_title, date_obj, lId)
			
	def getOne(self, browser, index):
		tmp_all_history = bh.get_browserhistory()
		tmp_browser_history_entry = tmp_all_history[browser][index]

		# convert date_string to datetime objs
		website_url, website_title, date_string = tmp_browser_history_entry
		date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
		short_url, lId = shorten(website_url)
		self.browser_entry = (short_url, website_title, date_obj, lId)

	# def getPrettyDateInfo(self, indicator): # indicator accepts a website url, website title, or datetime obj
	# 	# find entry with indicator
	# 	if type(indicator) == str:
	# 	prettyDatetime = 
	# 	return prettyTimeElapsed, prettyDatetime


if __name__ == '__main__':
	# kChrome()
	# h = History()
	# h.getAll('chrome', 100)
	# print(h.browser_history)