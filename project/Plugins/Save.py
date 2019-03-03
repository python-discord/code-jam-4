""" Contains logic for loading and saving states """
import json
import os
from project.utils import CONSTANTS
from project.ClipboardManager.ClipboardObject import ImageClipboardObject, TextClipboardObject

def saveState(location, clipboard):
	state = []
	image = 1
	for item in clipboard:
		print(item, type(item))
		if type(item) == TextClipboardObject:
			state.append({"type": "string", "content": str(item) })
		elif type(item) == ImageClipboardObject:
			imagelocation = "{0}/images/image{1}.png".format(os.path.dirname(location), image)
			state.append({"type": "image", "location": imagelocation})
			item.getImage().save(imagelocation, 'PNG')
			image += 1
	
	with open(location, 'w') as outfile:
		json.dump(state, outfile)

def loadState(state):
	pass