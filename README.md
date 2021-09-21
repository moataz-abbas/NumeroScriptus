# NumScriber
<p>Use touchscreen to write and generate images of numbers in your handwriting to be used in machine learning training. </p>
<p>Created with kivy on python</p>


<p>Use this app to create handwritten images of numbers from 0 to 9. These can be used to train machine learning alogrithms for text detection. This is my first trial at making android apps. It's based on Kivy Python.
The functionality can be expanded later on to encompass the alphabet and you can create your own personal dataset of any charater set.</p>

<p>At the moment this app has the following functionalities, in v3.6
	• App creates a folder tree with a folder for each number under images directory.
	• Shows numbers (target number) in random order in the top panel
	• Use touchscreen to write numbers 
	• Save the image in the respective folder according to the shown number, by Save button
	• The image file is in .png format with the the target number and another series of digits after letter 's' generated between 10000 and 99999 in the file name.
	• Clear the scribed digit with Clear button
	• Undo button, delete the images saved in the current session of app usage. It can be used to delete all the previous images that were saved serially from the last one to the first one.
	• You can't delete old images created in previous sessions.
	• Autosave switch, you can opt to make the app save the image as soon as you remove you finger or pen off the touchscreen. 
	• The exclude numbers '4' and '7' from autosave checkbox; it gives you the option to wait for you after removing you finger or pen during autosave mode, as these numbers can be written on more than one touch downs.
	• The app don't save any image unless you have written something 
	• If you write a number then decide to switch on the autosave, it will start as soon as you switch, provided you wrote something on the whiteboard.
	• Save and autosave doesn't work unless you attempt at writing something on the whiteboard.

I hope this could be of help, and I welcome any feedback, peace out.

</p>
<p>Update v 3.7:
	• Changed the function of the checkbox. Now the checkbox gives the option that in case the number to be scribed is 4 or 7, to choose between:
		○ Active: the autosave function will save after the second stroke of writing on the screen.
		○ Disabled: the autosave saves after the first stroke.
	• Autosave switch is on by default
	• Checkbox is active by default
</p>
<p>
Update 4.1:
	• The app doesn't register any scribing smaller than a certain threshold, attempting to ignore an accidental touch.
</p>
