#	- Reading and Writing data (Remy)
#		- Put the user input into Json file and read from Json file
#		- User input:
#			- Task = Variable name
#			- Task title and Description *			
#			- Date (Unix/Actual time date)
#			- Boolean variable for mark and unmark task
#
#		- Remove user input
#	Tsu Chiang will be passing over a list of list
#	I will have to loop through the list using

import json
import datetime

class readWrite:
	# curse = "Fuck You!"
	def __init__(self):
		self.data = {}
		self.data["task"] = []
		# self.title = ""
		# self.desc = ""
		# self.date = ""
		# self.done = ""

	def readInput(self):
		l = []
		with open("taskList.txt") as json_file:
			data = json.load(json_file)
			for t in data["task"]:
				print("Title: " + t["Title"])
				print("Description: " + t["Description"])
				print("Deadline: " + t["Deadline"])
				# print("Completed: " + t["done"])
				l.append(t)
		json_file.close()
		print ("l is : ", l)
	# def writeInput(self, title, desc, date, done):
	def writeInput(self, title, desc, date):
		self.data["task"].append({
			"Title": title,
			"Description": desc,
			"Deadline": str(date),
			# "done": done
		})
		# print(curse)
		
	def	writeFile(self):
		with open("taskList.txt", "w") as outfile:
			json.dump(self.data, outfile, indent = 4)

t = datetime.datetime.now()
t1 = readWrite()
# t1.writeInput("task 1", "Copy Hello World", str(t), "1")
# t1.writeInput("task 2", "Paste Hello World", str(t), "1")
# t1.writeInput("task 3", "Modify Hello World", str(t), "1")
# print(t1.curse)
t1.writeInput("task 1", "Copy Hello World", str(t))
t1.writeInput("task 2", "Paste Hello World", str(t))
t1.writeInput("task 3", "Modify Hello World", str(t))

t1.writeFile()
t1.readInput()
print("\n")
