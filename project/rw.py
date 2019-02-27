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
	# def __init__(self, title, desc, date, done):
	def __init__(self):
		# self.task = []
		# self.title = title
		# self.desc = desc
		# self.date = date
		# self.done = done
		
		self.title = ""
		self.desc = ""
		self.date = ""
		self.done = ""
		
	# def openFile(pJson):
		# print(json.dumps(pJson, indent=4))
		# f = open("taskList.json", "a")
		# f.write(json.dumps(pJson, indent=4))
		# f.close()
		
	def readInput(self):
		# print("This is to read input")
		# print("Printing...")
		# print("Title: " + self.title)
		# print("Description: " + self.desc)
		# print("Task: " + self.task)
		# print("Date: " + str(self.date))
		# print("Done: " + self.done)
		# print("\n")
		
		# f = open("taskList.json", "r")
		
		# myList = json.loads(f.read())
		# myList = json.loads(f.read())
		
		# with open('taskList.json') as json_file:
			# data = json.load(json_file)
			# for p in data['people']:
				
		
		# print("Printing List in List")
		
		# for x in myList:
			# print(x)

			
		with open("taskList.txt") as json_file:
			rJson = json.load(json_file)
			for t in rJson["task"]:
				print("Title: " + t["title"])
				print("Description: " + t["desc"])
				print("Due: " + t["date"])
				print("Completed: " + t["done"])
				print("\n")
		
		print("\n")


		# print("Printing from json...")
		# print(x["title"])
		# print(x["desc"])
		# print(x["task"])
		# print(x["date"])
		# print(x["done"])
		# print("\n")
		
	def writeInput(self, title, desc, date, done):
		# print("This is to write input")
		# print("Printing...")
		# print("Title: " + title)
		# print("Description: " + desc)
		# print("Date: " + str(date))
		# print("Done: " + done)
		# print("\n")
		
		# pJson = {
			# "title": self.title,
			# "desc": self.desc,
			# "task": self.task,
			# "date": str(self.date),
			# "done": self.done
		# }
		# print(json.dumps(pJson, indent=4))
		# f = open("taskList.json", "w")
		# f.write(json.dumps(pJson, indent=4))
		# f.close()
		# print("\n")
		# openFile(pJson)
		
		wJson = {}
		wJson["task"] = []
		wJson["task"].append({
			"title": title,
			"desc": desc,
			"Date": str(date),
			"done": done
		})
		
		print(json.dumps(wJson, indent = 4))
		
	def	writeFile(wJson):
		with open("taskList.txt", "w") as outfile:
			json.dump(wJson, outfile, indent = 4)

t = datetime.datetime.now()
# print(t)
# print("\n")
# print(t.strftime('%d/%m/%Y'))
# print("\n")
# t1 = readWrite("New title", "New Description", "Printing Hello World", t.strftime('%d/%m/%Y'), "0")

# t1 = readWrite("New title", "New Description", "Printing Hello World", t, "0")

t1 = readWrite()

t1.writeInput("task 1", "Copy Hello World", str(t), "1")
t1.writeInput("task 2", "Paste Hello World", str(t), "1")
t1.writeInput("task 3", "Modify Hello World", str(t), "1")
t1.writeFile()
# t1.readInput()
print("\n")
