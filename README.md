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

Slithering Snacks's submission for the 4th code jam.

Qt, via PySide2 ("Qt for Python"), is used as the GUI framework. The Qt Multimedia module is an easy, cross-platform solution to playing media. The UI windows are designed in Qt Creator and then converted to Python using `pyside2-uic`.

SQLite is used to drive a database which persists the media playlist.

## Description

A basic media player with the following features:

    * Previous and next navigation of playlist
    * Seeking
    * Persistent and sortable playlist
    * Parsing and displaying metadata tags of media

## Setup & Installation

First, make sure [ffmpeg](https://ffmpeg.org/) is installed. Particularily, this program relies on `ffprobe`. It should either be on your `PATH` or in the current working directory when running the program.

Open a terminal in the repository's root directory and execute the following command to install the project's dependencies:

```bash
pipenv --sync
```

To run the program, execute

```bash
pipenv run start
```

## How do I use this thing?

#### Adding media
Click on `File` in the menu bar, then click on `Add files`. In the file dialogue which opens, browse for and select the media to add to the playlist.

#### Removing media
Right click on a row in the playlist, select the `Remove` action on the context menu, and confirm removal in the prompts which appear.

#### Playing media
Click on the `Play` button to start playing media. To pause, click on the same button again. Notice that when media is playing, the button changes from `Play` to `Pause`. The `Previous` and `Next` may be used to navigate the playlist.

The time remaining on the current song can be seen below the playlist, to the left of the slider. It display the remaining time in hexadecimal.

#### Seeking
Click on the slider below the playlist to seek. In the dialogue that opens, use the dials to select the hour, minute, and second you wish to seek. Note that the values below the dials are _octal_ numbers.

#### Playlist
Media can be sorted on the playlist by clicking on the column headers. An indicator appears on the header by which the playlist is being sorted.
