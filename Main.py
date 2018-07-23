import Functions
import queue
import threading

class QuitProgram(Exception): pass
class UnknownCommand(Exception): 
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg

while True:

	#gmail_account = Functions.setup()
	#gmail_data = Functions.getdata(gmail_account)


	gmail_account = Functions.setup()
	my_queue = queue.Queue()
	t2 = threading.Thread(target=Functions.getdata, args=(gmail_account,my_queue))
	t1 = threading.Thread(target=Functions.loading, args = (t2,))
	t2.start()
	t1.start()
	t2.join()
	t1.join()
	#gmail_data = Functions.getdata(gmail_account)
	
  logged_in = True
	gmail_data = my_queue.get()
	Functions.help()
	while logged_in:
		try: 

			cmd = input("\nPlease enter a command: ")

      if cmd.lower() == "csv":
				Functions.create_csv(gmail_data)
			elif cmd.lower() == "graph":
				Functions.graph_total()
			elif cmd.lower() == "count":
				usr = input("Enter <email address> or <total>: ")
				n = Functions.count(usr,gmail_data)
				print(str(n))
			elif cmd.lower() == "logout":
				Functions.logout()
				logged_in = False
			elif cmd.lower() == "print":
				usr = input("Enter <email address> or <total>: ")
				Functions.printMessages(usr,gmail_data)
			elif cmd.lower() == "quit":
				raise QuitProgram
			elif cmd.lower() == "help":
				Functions.help()
			else:
        raise UnknownCommand("Invalid command '" + cmd +"'; type 'help' for commands")
        
		except FileNotFoundError:
			print("You have to create a CSV before making a graph.")
		except UnknownCommand as e:
			print(e.msg)
		except QuitProgram:
			break

	if logged_in == False:
		try:
			ans = input("Would you like to log back in? y/n ")
			if ans == "n":
				break
			elif ans == 'y':
				continue
			else:
				raise UnknownCommand("Please type 'y' or 'n'")
		except UnknownCommand as f:
			print(f)
	else:
		Functions.logout()
		break
