class Message(object):
	def __init__(self, messageDictionary):
		self._subject = messageDictionary['Subject']
		self._dateRecieved = messageDictionary['Date']
		self._sender = messageDictionary['Sender']

	# Override the str 
	def __str__(self):
		return "\n     Sender: " + str(self._sender) +"\n     Subject: " + str(self._subject)


class GMessage(Message):
	def __init__(self, messageDictionary):
		super().__init__(messageDictionary)
		self._date = messageDictionary['Date']
		self._messageDictionary = messageDictionary

	def getDictionary(self):
		return self._messageDictionary

	# Call
	def __str__(self):
		return super().__str__() + "\n     Date: " + str(self._date) + "\n"

	def getSender(self):
		return self._sender
		