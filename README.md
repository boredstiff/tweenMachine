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
