import numpy as np
import matplotlib.pyplot as plt
#the collections module is a part of Python 3.6 and is useful for counting things
import collections

#ignores enconding errors, for now
CSVfile = open("MessageCSV.csv", errors='ignore')
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

