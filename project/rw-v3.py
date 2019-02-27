import json
import datetime

class readWrite:
	def __init__(self):
		self.data = {}
		self.data["task"] = []

	def readInput(self):
		l = []
		with open("taskList.txt") as json_file:
			data = json.load(json_file)
			for t in data["task"]:
				print("Title: " + t["Title"])
				print("Description: " + t["Description"])
				print("Deadline: " + t["Deadline"])
				l.append(t)
		json_file.close()
		print ("l is : ", l)

	def writeInput(self, title, desc, date):
		self.data["task"].append({
			"Title": title,
			"Description": desc,
			"Deadline": str(date),
		})
		
	def	writeFile(self):
		with open("taskList.txt", "w") as outfile:
			json.dump(self.data, outfile, indent = 4)