# Code Jam IV: This app hates you!

The theme for this code jam will be **This app hates you!**. You will be creating an application using a GUI library of your choice in Python. The application must serve a real purpose, but must also fit the theme.

You can use any GUI library that you wish to use, but you have to make _a desktop app_. For example, you may use frameworks like PySide, PyQt, tkinter, or wxPython. You can even use stuff like Kivy or PyGame, although we do not recommend that you do. You may not, however, use webframeworks like Django or Flask, and you may not use anything that turns HTML and CSS into a desktop app that runs as a browser. 

Here are a couple of examples of what we mean by an application that "serves a real purpose but also fits the theme":
* A calculator app that calculates the right answers, but represents the answer in a way that's completely impractical.
* An image resizer where you have to specify which part of the image to resize, specify how much force to apply to the resize operation in newtons, and then manually resize the image by turning a crank.
* An alarm clock app that plays a very loud sound effect every 5 minutes reminding you that your alarm will ring in 6 hours. The closer it gets to the 6 hour mark, the lower the volume of the sound effect. When the time is up, the sound effect is virtually inaudible.

Remember that teamwork is not optional for our code jams - You must find a way to work together. For this jam, we've assigned a leader for each team based on their responses to the application form. Remember to listen to your leader, and communicate with the rest of your team! 

**Remember to provide instructions on how to set up and run your app at the bottom of this README**.

# Tips

* Please lint your code, and listen to the linter. We recommend **flake8**, and you can use `pipenv run lint` to run it. We will be evaluating your style, and unlinted code will lead to point deductions.
* Remember to work closely with the rest of your team. We will deduct points for poor teamwork.
* Don't overcomplicate this. It's better to write a relatively simple app that is 100% feature complete than failing to finish a more ambitious project.
* For information on how the Code Jam will be judged, please see [this document](https://wiki.pythondiscord.com/wiki/jams/judging).

# Setting Up

You should be using [Pipenv](https://pipenv.readthedocs.io/en/latest/). Take a look 
[at the documentation](https://pipenv.readthedocs.io/en/latest/) if you've never used it before. In short:

* Setting up for development: `pipenv install --dev`
* Running the application (assuming you use our project layout): `pipenv run start`

# Project Information
##### Team Name

Knowledgeable Kois

##### Members

[BWACPro](https://github.com/BWACpro)

[kaleidawave](https://github.com/kaleidawave)

[Transfusion](https://github.com/Transfusion) 👑
## Description

### Theme
Clipboard Mangler

### What does it do?
It's a clipboard manager in all its usefulness:

   - For when you `Ctrl-Z` but have no way to redo
   - For when you need to quickly swap items in and out of the clipboard
   - For when you need images and text to be quickly accessible at the same time
   - ...etc
   
However, it has a mind of its own...

### Feature Breakdown
#### Core
* ~~Hooks into Ctrl-C, Ctrl-X and Ctrl-V~~ **done!**
* Able to select specific copied items and modify them 
  * Able to edit copied text
  * ~~Able to add and remove copied items~~ **done!**
  * ~~Able to rearrange copied items~~ **done!**
  * ~~Able to delete specific items~~ **done!**
* ~~Clipboard should be saved after exiting the app~~ **done!**
* _(Keep entire clipboard history as a stack too?)_
* _(Tray Logo, from which we can access settings?)_
#### Crappifying
* Plugin-based architecture, each crappifier should be a class which applies its own transformation onto an image or text
* Ideas for text
  * ~~Misspell words~~ **done!**
  * Randomly transpose words around
  * ~~Replace entire blocks of text with "funny" copypasta from APIs~~ **done!**
* Ideas for images
  * Deep fry and load back into memory
  * ~~Randomly rotate~~ **done!**
  * Randomly add meme images to the front of the clipboard
* ~~Randomly select transformations to apply.~~ **done!**

## Setup & Installation

Clone this repo, in a terminal run `pipenv install` then `pipenv run start`

Unit tests are written using the [pytest](https://docs.pytest.org/en/latest/) framework. 

`pipenv run test` runs the available tests.

## How do I use this thing?

As you copy and paste text or images, the copied content will be added to the scroll area of the main window.

The numbers on the left, indicated by ③ in the infographic below indicate their position in the list of copied items.

A selected item, ① in the infographic below, has a different background color compared to other items. After selection, it may be moved up or down the list, i.e. swapped with the item above or below it, as shown by ②. Remove removes the selected item.

This may be useful if you want to organize your frequently accessed items at the top. Unchecking the `Always load top item into clipboard` option in the Settings menu will automatically copy the selected item into the system's clipboard.

Saving the state of the clipboard is done automatically if the option in Settings is checked, or may be done manually in the File menu.
![Screenshot of Clipboard Mangler on macOS Mojave](https://i.imgur.com/FbxCbjF.png)

## Documentation

Documentation is generated using [Sphinx](http://www.sphinx-doc.org/en/master/). To build:
```sh
cd docs
sphinx-apidoc -f -o source/ ../project/
make html
```
