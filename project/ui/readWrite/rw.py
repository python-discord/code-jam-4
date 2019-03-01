import json
import os
# import datetime

class readWrite:
	def __init__(self):
                self.data = []

	def readInput(self):
		if os.path.exists("taskList.txt"):
			if os.stat("taskList.txt").st_size < 1:
				return []
			else:
				with open("taskList.txt") as json_file:
					data = json.load(json_file)
				json_file.close()
				return data
		else:
			f = open("taskList.txt", "x")
			return []

	def writeInput(self, title, desc, date, mark):
		self.data.append({
			"Title": title,
			"Description": desc,
			"Deadline": str(date),
			"Mark": mark
		})
		
	def writeFile(self, data):
		with open("taskList.txt", "w") as outfile:
                        for i in data:
                                json.dump(i, outfile, indent = 4)
			
		outfile.close()
