# Note Extractor!

## Instructions
* Open the program (probably the windows64 executable)
* Use the file selector to grab an image of a page of sheet music (works with jpg, png, and tiff. maybe also others, I didn't check.)
* Use the **I and K keys** to set the window size. To calibrate, center the mouse on the dot of a quarter note and adjust the size until there is a very small amount of space above or below the stick.
* Select the type of note you want to indicate by pressing (q)uarter, (w)hole, (e)ighth or (h)alf. You can also select half note by pressing r so that as you're moving through the sheet music you don't have to move your left hand.
* Click on the center of the note's dot
  * If you misclick, clicking a second time inside a box will delete that box.
  * You can use the arrow keys to nudge the position of the most recently placed box
* When you're done labeling notes, press ENTER and all the images will be saved to a new folder called training_notes which will be created in the same directory as the executable if it doesn't exist already.

Alternately, if you press 'n', it'll make a new box near the last box placed. (The first box still has to be placed with the mouse)

## Notes
* The newly created image files will be named using the format "imagename_quarter_0.png"
* When you run the program, the sheet music will be scaled to the largest size that still fits on your screen. When you press enter to save, the saved images will be in the original resolution, not the scaled down resolution.
