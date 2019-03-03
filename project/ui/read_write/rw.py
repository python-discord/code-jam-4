import json
import os


class ReadWrite:
    def __init__(self):
        self.data = []

    def read_input(self):
        if os.path.exists("taskList.json"):
            if os.stat("taskList.json").st_size < 1:
                return []
            else:
                with open("taskList.json") as json_file:
                    data = json.load(json_file)
                json_file.close()
                return data
        else:
            f = open("taskList.json", "x")
            f.close()
            return []

    def write_input(self, title, desc, date, mark):
        self.data.append({
            "Title": title,
            "Description": desc,
            "Deadline": str(date),
            "Mark": mark
        })

    def write_file(self, data):
        with open("taskList.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
