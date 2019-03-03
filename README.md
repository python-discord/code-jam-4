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

High Tech Keyboard (HTT), a High Houses company (of the Adorable corperation)

## Description

"Hello there! This is the High Tech Text Editor. Did you know that the first keyboard was invented in 1868? That was a long time ago!

Here at Adorable Laboratories, we don't live in 1868 anymore, so we believe in giving our users more modern features than they could ever need. And when you think of modern, accessible, and afforadable, what first comes to mind?  Why lootboxes, of course!

Therefore, we are proud to introduce the first high-tech, personalized onscreen keyboard text editor with a built-in progression system! Go ahead, check it out!

## Setup & Installation

Do to difficulties installing PyAudio with pip, there are some additional steps you may need to take if you encounter an error.
If you are using Windows x32, you can run `pipenv install --dev` and then `pipenv run start`.
If you are using a different OS, or if you are unable to run the pipenv install, you must manually install the dependencies found in the Pipfile and run project/__main__.py instead.
PyAudio installation instructions for your OS can be found at the [PyAudio Homepage](https://people.csail.mit.edu/hubert/pyaudio/).

## How do I use this thing?

Our tutorial will guide you! Here's a brief rundown:
* Type words to get XP!
* Use XP to unlock lootboxes!
* Open lootboxes to get more keyboard keys!
* Use new keyboard keys to type new words!
