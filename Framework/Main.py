import Functions

class QuitProgram(Exception): pass

while True:
	gmail_account = Functions.setup()
	gmail_data = Functions.getdata(gmail_account)
	logged_in = True
	while logged_in:
		try: 
			cmd = input("\nPlease enter a command:\n  CSV: to create csv of gmail data\n  COUNT: count emails\n LOGOUT: to logout\n GRAPH: to generate graph\n\n")
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