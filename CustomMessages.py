class Message(object):

	

	## Want to pass the entire dictionary and then unpack here but screw it...
	## **kwargs says argument1 must be str, not dict
	def __init__(self, messageDictionary):

		# self.subject = subject
		# self.sender = sender

		# print("in CustomMessage")
		# print(self.subject)
		# print(self.sender)



		self.subject = messageDictionary['Subject']
		self.dateRecieved = messageDictionary['Date']
		self.sender = messageDictionary['Sender']

		# for key, value in kwargs.iteritems():
		# 	setattr(self, key, value)

	def __str__(self):
		return "From Class: Message\n     Subject: " + str(self.sender) +"\n     Sender: " + str(self.subject)


		



## GMessage's are special because they have a date... wow.
class GMessage(Message):
	def __init__(self, messageDictionary):
		super().__init__(messageDictionary)
		self.date = messageDictionary['Date']

	def __str__(self):
		return super().__str__() + "\nFrom Class: GMessage\n     Date: " + str(self.date)