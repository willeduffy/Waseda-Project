import Functions
import queue
import threading

class QuitProgram(Exception): pass

while True:

	gmail_account = Functions.setup()
	my_queue = queue.Queue()
	t2 = threading.Thread(target=Functions.getdata, args=(gmail_account,my_queue))
	t1 = threading.Thread(target=Functions.loadbar, args = (t2,))
	t2.start()
	t1.start()
	t2.join()
	t1.join()
	#gmail_data = Functions.getdata(gmail_account)
	logged_in = True
	gmail_data = my_queue.get()

	while logged_in:
		try: 
			cmd = input("\nPlease enter a command:\n  CSV: to create csv of gmail data\n  COUNT: count emails\n LOGOUT: to logout\n GRAPH: to generate graph\n PRINT: to print emails\n\n")
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
			else:
				print("Please enter a valid command.")
		except QuitProgram:
			break
	ans = input("Would you like to login? y/n")
	if ans == "n":
		break
Functions.logout()