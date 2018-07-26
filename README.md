# TweenMachine

---------------------
### The easiest way to create breakdown poses in Maya

Say you’re creating poses for your character with stepped keys, and have created key poses on frames 1 and 10.
You want to make a breakdown pose on frame 7, but you want it to favor the first pose by 70%. The following comparison
shows how this would be accomplished both with and without tweenMachine.

|Manual Process                                  | Tween Machine                                        |
|------------------------------------------------|------------------------------------------------------|
|Select all controls on the character            | Select all controls on the character                 |
|Change interpolation on all keyframes to linear | Left-click on frame 7 in the timeline                |
|Left-click on frame 3 in the timeline           | Adjust a slider in the tweenMachine interface to -70 |
|Middle-click on frame 7 in the timeline         |                                                      |
|Set a key                                       |                                                      |
|Change interpolation on all keyframes to stepped|                                                      |


If you’re not happy with the results, you’ve got a lot of steps to repeat if you’re doing it the manual way. With 
tweenMachine, you simply adjust the slider and see the results immediately.  Better still, if you’ve created a custom
set that controls the entire character, you can skip the first step and save even more time.

Will tweenMachine create perfect breakdown poses? Not likely, but it will get you closer to your goal a lot faster than
other methods. You spend less time with busywork and more time making actual progress.

Tween Machine was originally developed by [Justin Barrett](http://www.justinsbarrett.com/) and used extensively throughout
the animation and visual effects industries for years. 

Development was taken over by [Alex Widener](https://github.com/alexwidener) in February 2018. 

| Contribution                     | Author                                              |
|----------------------------------|-----------------------------------------------------|
|tweenMachine.mel/ tweenMachine.py | [Justin S. Barrett](http://www.justinsbarrett.com/) |
|xml_lib.mel                       | J. Adrian Herbez                                    |
|Maya Shelf Icon                   | [Keith Lango](http://keithlango.squarespace.com/)   |


## Updates
Subscribe to very infrequent and non-spammy email updates about new versions [at this link](https://github.us18.list-manage.com/subscribe?u=21f14bb7b1c884b7f2d517b57&id=a966b6ab32).

## Installation

Animators: Do not copy the file listed directly above, as tweenMachine is in active development and will be for the next few weeks. Instead, go to the [Releases](https://github.com/alexwidener/tweenMachine/releases) tab above the files, and download version 3.0.0.

Version 3.1.0 will come out at some point and be a restructure/rewrite/with many new features and a new look. Please check back for updates. 

### Windows:

Move the tweenMachine.py file to your default Maya scripts directory.

`C:/Users/username/Documents/maya/version_number/scripts`

Save the icon into the “prefs/icons” folder for the same Maya version.

`C:/Users/username/Documents/maya/version_number/prefs/icon`

Once everything is installed, open Maya. In the script editor, type the following in a Python tab:

```
import tweenMachine
tweenMachine.start()
```

Highlight the line, then select `File–>Save Selected to Shelf` to turn it into a shelf button. Use the Shelf Editor to
assign the icon to the shelf button.

### Mac OS:

Move the tweenMachine.py file to your default Maya scripts directory.

`/Users/username/Library/Preferences/Autodesk/maya/version_number/scripts`

Save the icon into the “prefs/icons” folder for the same Maya version.

`/Users/username/Library/Preferences/Autodesk/maya/version_number/prefs/icon`


Once everything is installed, open Maya. In the script editor, type the following in a Python tab:

```
import tweenMachine
tweenMachine.start()
```

Highlight the line, then select `File–>Save Selected to Shelf` to turn it into a shelf button. Use the Shelf Editor to
assign the icon to the shelf button.

### Linux
Do all the same stuff wherever your maya scripts folder is. You can find it by entering the following in a Maya Script Editor:

```
import sys
for s in sys.path:
    print(s)
```

And then find the `maya/version_number/scripts/` folder and follow the same steps as above. 

## Usage

When running tweenMachine for the first time, it will open with a bare-bones interface. There’s a single slider labeled
“Selected”, and a group of seven buttons below the slider. In this mode, tweenMachine operates only on selected objects.
Click between two keys on the timeline, and adjust the “Selected” slider to create a new breakdown key. The values set
for the new breakdown key will be biased toward the surrounding keys on the timeline based on how you set the slider.
In the slider’s default position, the new keys will be exactly halfway between the surrounding keys. Slider values to
the left will favor the new key toward the previous key, while values to the right will favor the next key. Clicking one
of the buttons will set the slider to a preset value. If you wish, you can highlight individual channels in Maya’s
channel box, and tweenMachine will only perform its work on those channels, leaving others untouched.

That covers the core operation of tweenMachine, but there are additional features available through various menu items. A full breakdown of all menu items is covered in the next section

### Menu

The functions for all (currently available) tweenMachine menu items are as follows…

`Options > Show`

Contains Menu Bar and Label visibility toggles, plus radio buttons that let you select if you want to see the slider,
the buttons, or both.

`Options > Mode… > Window`

Sets the interface to be a standard floating window.

`Options > Mode… > Toolbar`

Sets the interface to toolbar mode, allowing you to place it next to other Maya toolbars in the main window.

`Options > Overshoot`

Toggles “overshoot mode” for all sliders. By default, the range of all sliders is -100 to 100. When “overshoot mode” is
active, the range of all sliders changes to -150 to 150. Using this mode allows you to create overshoot poses on the
right end of the sliders in the 101-150 range, while using it in the -101 to -150 range on the left end effectively
creates anticipation poses.

`Options > Special Tick Color`

Toggles the tick color used for keys added using the tweenMachine. When off (default), the standard tick color is used.
When on, the “special” tick color is used.

### Buttons

The buttons below each set slider provide a quick way to set the slider to predictable values. By default they are set
to mimic the style of pose favoring familiar to 2D animators. The center button is an exact halfway point between the
two poses, and spreading out from the center on either side, the remaining buttons represent pose favoring by 1/3, 1/5,
and 1/8 in their respective directions.By holding the mouse over any button, an annotation popup will appear showing the
numerical value assigned to that button.

While the button values and colors are locked in this version (unless you manually tweak them), the Python version will
eventually allow them to be easily customized.
