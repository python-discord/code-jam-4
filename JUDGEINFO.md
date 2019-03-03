# To the judges

Thank you for all the time you take helping run the PyDis code jams and server.

Although our team would **love** to see you suffer with our program, we do not wanna be marked down for stuff so here's is a list of *(hopefully)* everything that is so-called "evil" with our program.

**Since we would love for you to experience this blind, please only read this once you've seen the app for the first time so you may see the evilness we managed to achieve.**


## The Main Program

As you have likely already seen, this paint tool isn't your average program. The canvas is completely noninteractive. You are required to use the sidebar to enter the values.

For the *X* and *Y* entries (see **The Language** to translate the labels), you must enter the X and Y value of the pixel you would like to colour, with `(0,0)` being the top-left corner.

The *Colour* entry is a bit special. It works like this

* Grab the colour you would like to enter
* Find its hex value
* Swap the last two digits and the first two digits around (so it's in BGR format instead of RGB)
* Convert it into denary / base 10
* Enter your final answer into the Entry box

## The Language

The entire project is written in Katakana, a Japanese syllabary, which when pronounced sounds similar to the English equivalent. This was in order to make the program more difficult to use.

However, as an easter egg, we included a method to translate the entire program into English and to do this, you need to enter the Konami code.

Entering **Up, Up, Down, Down, Left, Right, Left, Right, B, A, ~~Start~~ Return** in quick succession will translate the entire program from Katakana to English.

## Saving

The "Save Processor Time" button destroys the program. Having already gone through the application, you may have discovered this. 
In order to save, use `Alt + F4` (or the X button) to save your file to a file select window. However I suggest you save small files, since a button needs to be pressed for every byte saved. For example, a 2x2 image contains 75 bytes, meaning that you'd need to press the button 75 times.

## Small, slightly inconvenient things
It's the small things that everyone hate :D

### Undo & Redo

To fit the theme, the *Undo* and *Redo* buttons have been switched around, so clicking one will trigger the other. This also applies to keybinds. Using `Ctrl + Z` will redo the previous action and Using `Ctrl + Y` or `Ctrl + Shift + Z` will undo the action.

### Open File

To open a file, navigate to the *Close* button (ironically) and choose a file. There's no saying what will happen to your file though... Maybe it will:
* Become super pixelated
* Have completely different colours to the original image
* Become fragmented
* Have a complete shuffle of pixels
* Be absolutely normal

Which one will happen? The computer will decide... you have no control.
Not only that, but the larger the image, the longer it'll take to load, ensuring that any haste is completely obliterated.
Also, in massive folders, it doesn't scroll so good luck finding that one file at the bottom!


### New File

To create a new file, use the *New File* button and specify a height and width. Don't think you're off the hook because the label is correct. Legends say that your height and width may be switched around...

