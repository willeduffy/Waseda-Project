from __future__ import print_function
from googleapiclient.discovery import build
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

import CustomMessages


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
		

		newMessage = CustomMessages.GMessage(temp_dict)

		# print()
		# print(newMessage)
		final_list.append(newMessage) # This will create a dictonary item in the final list
		
		# final_list.append(temp_dict) # This will create a dictonary item in the final list

	return final_list

#by Will
#data will be the list returned by the getdata(gmail) function
def create_csv(data):

 
	#creates CSV file and exports the values as .csv
        #utilizes CSV library
	with open('MessageCSV.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
	    fieldnames = ['Sender','Subject','Date','Snippet']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
	    writer.writeheader()
	    for val in data:
	    	writer.writerow(val.getDictionary())

#by Will
def graph_total():
        #ignores enconding errors
        CSVfile = open("MessageCSV.csv", errors='ignore')
        CSVfile.readline() #skips first line of csv

        #sendersList will become list of senders' email addresses
        sendersList = []
        #gets data right from CSV
        for line in CSVfile:
            items = line.strip().split(",")
            sender = str(items[0])

            sendersList.append(sender)

        #uses the collections library to make a Counter object -- similar to a dictionary
        frequencyCounter = collections.Counter(sendersList)

        #get lists of the keys and values of the dictionary
        senders = list(frequencyCounter.keys())
        frequency = list(frequencyCounter.values())
            
        fig1, ax1 = plt.subplots()

        #generates pie chart using matplotlib
        #doesn't show labels on pie wedges anymore
        ax1.pie(frequency, autopct='%1.1f%%', startangle=90, shadow = False, pctdistance=0.85)

        #draws white circle at the center to make it look nice
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        #equal aspect ratio ensures that pie is drawn as a circle
        ax1.axis('equal')  
        plt.tight_layout()

        #saves pie chart as .png
        plt.savefig("MessagesGraph.png")

        #generates key for pie chart -- this makes it easier to see a lot of different senders
        #currently can't get key to display nicely in saved .png -- will try to fix later
        patches, texts = plt.pie(frequency, shadow=False, startangle=90)
        plt.legend(patches, senders, loc="best")
        
        plt.show()

        #saves something to a text file
        #not useful right now -- will come back later
        graphText = open("GraphText.txt", "w")
        for i in senders:
                for q in frequency:
                        graphText.write(i +": " + str(q))
        graphText.close()
        


# By Dustyn and Will
# User is the email address entered
# data is the list of GMessage objects
def printMessages(user, data):

	print("User: ")
	print(user)

	# print("Data:" )
	# print(data)
	if user == "total":
		for email in data:
			print(email)
	
	# Need to parse email from between the < >
	else:
		for email in data:
			print(email.getSender())
			if email.getSender() == user:
				print(email)




# Count does not work for specific email address as of 7/18 
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


