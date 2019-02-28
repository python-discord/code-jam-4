import json
import datetime

class readWrite:
	def __init__(self):
		self.data = []

	def readInput(self):
		l = []
		with open("taskList.txt") as json_file:
			data = json.load(json_file)
		json_file.close()

	def writeInput(self, title, desc, date, mark):
		self.data.append({
			"Title": title,
			"Description": desc,
			"Deadline": str(date),
			"Mark": mark
		})
		
	def	writeFile(self):
		with open("taskList.txt", "w") as outfile:
			json.dump(self.data, outfile, indent = 4)
			
		outfile.close()