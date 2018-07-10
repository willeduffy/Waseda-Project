from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
import time
import dateutil.parser as parser
from datetime import datetime
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import collections


def setup():
	# Setup the Gmail API
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		    creds = tools.run_flow(flow, store)
	service = build('gmail', 'v1', http=creds.authorize(Http()))
	return service

def getdata(gmail):
	# Call the Gmail API
	# all_messages is a dictionary with one key/value pair -- "messages": 
	# [list of dictionaries containing, threadId, and their corresponding values]
	all_messages = gmail.users().messages().list(userId='me').execute()
	mssg_list = all_messages["messages"]
	final_list = []
	for mssg in mssg_list:
		temp_dict = { }
		m_id = mssg['id'] # get id of individual message
		message = gmail.users().messages().get(userId="me", id=m_id).execute() # fetch the message using API
		payld = message['payload'] # get payload of the message 
		headr = payld['headers'] # get header of the payload

		for one in headr: # getting the Subject
			if one['name'] == 'Subject':
				msg_subject = one['value']
				temp_dict['Subject'] = msg_subject
			else:
				pass
		for two in headr: # getting the date
			if two['name'] == 'Date':
				msg_date = two['value']
				date_parse = (parser.parse(msg_date))
				m_date = (date_parse.date())
				temp_dict['Date'] = str(m_date)
			else:
				pass
		for three in headr: # getting the Sender
			if three['name'] == 'From':
				msg_from = three['value']
				temp_dict['Sender'] = msg_from
			else:
				pass

		temp_dict['Snippet'] = message['snippet'] # fetching message snippet
		final_list.append(temp_dict) # This will create a dictonary item in the final list
	return final_list


def create_csv(data):
	#Creates CSV file and exports the values as .csv
	with open('MessageCSV.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
	    fieldnames = ['Sender','Subject','Date','Snippet']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
	    writer.writeheader()
	    for val in data:
	    	writer.writerow(val)

def graph_total():
	#ignores enconding errors, for now
	CSVfile = open("MessageCSV.csv",errors="ignore")
	CSVfile.readline() #skips first line of csv

	sendersList = []
	for line in CSVfile:
	    items = line.strip().split(",")
	    sender = str(items[0])
	    sendersList.append(sender)

	#Uses the collections library to make a Counter object -- similar to a dictionary
	frequencyCounter = collections.Counter(sendersList)
	#Get lists of the keys and values of the dictionary
	#Order?
	senders = list(frequencyCounter.keys())
	frequency = list(frequencyCounter.values())
	fig = plt.figure(1,figsize=(18,5))  #Numbers in parentheses determine the dimensions of the plot
	ax1=fig.add_subplot(111)            #11 Means make a grid 1 plot box wide by 1 box tall.  
	                                    #The final 1 means let ax1 be the first plot box.
	#Generates a list [0, len(senders)-1] counting by 1
	x_pos = np.arange(len(senders))
	plt.bar(x_pos, frequency, align='center', alpha=0.5)
	#places each item of senders at x position [0, len(semders)-1]
	plt.xticks(x_pos, senders)
	plt.ylabel('Number of emails')
	plt.title('Emails received from specific senders')
	plt.show()



def count(name,data):
	num = 0
	if name == "total":
		for email in data:
			num += 1
		return num
	else:
		for email in data:
			if email['Sender'] == name:
				num += 1
	return num

def logout():
	os.remove("credentials.json")


