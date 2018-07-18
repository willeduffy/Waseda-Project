class Message(object):
	def __init__(self, messageDictionary):
		self.subject = messageDictionary['Subject']
		self.dateRecieved = messageDictionary['Date']
		self.sender = messageDictionary['Sender']

	# Override the str 
	def __str__(self):
		return "\n     Sender: " + str(self.sender) +"\n     Subject: " + str(self.subject)


class GMessage(Message):
	def __init__(self, messageDictionary):
		super().__init__(messageDictionary)
		self.date = messageDictionary['Date']
		self.messageDictionary = messageDictionary

	def getDictionary(self):
		return self.messageDictionary

	# Call
	def __str__(self):
		return super().__str__() + "\n     Date: " + str(self.date) + "\n"

	def getSender(self):
		return self.sender
		