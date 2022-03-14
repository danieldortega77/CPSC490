Setting up virtual environment:
py -m venv 490-venv
(py, python, python3)

Activating venv:

Windows:
490-venv\Scripts\activate.bat

MacOS/Unix:
source 490-venv/bin/activate

Installing packages:
python -m pip install pyOSC3

Deactivating venv:
deactivate


OSC Message received by SC in format
message:    [ /print, 440 ]
time:       760.7525028
address:    a NetAddr(127.0.0.1, 55935)
port:       57120

log:

2/19 (2 hours)
Going through pygame tutorial
https://www.youtube.com/watch?v=FfWpgLFMI7w

2/21 (5 hours)
Add modes for drawing and/or removing walls, start, and finish
Play pitch in OSC according to note on the grid

2/26 (5 hours)
Play correct pitch according to note
Add visual indication that node was visited over time

2/28 (5 hours)
Add comments throughout code
Make window scalable

3/6 (4 hours)
Disallow changes while simulation is running
Add text info on current algorithm and draw mode
Made pluck sound instead of constant tone

3/7 (4 hours)
Stop continuous running (bug fix)
Reset rather than have random grid after pathfinding finishes

3/13 (5 hours)
Add instrument switching
Consolidate the text render into a separate function
Change how algorithm is selected (cycle with Tab instead of individual keys for each)

3/14 (5 hours)
Add selection mode
Add deselection mode
Keybind to clear selection
Type pitch for selected notes = *editable text for each cell!*

TODO:
Change color scheme?
Option to "increase" note for selection?
Higher octaves
Panning based on grid location? Or relation to start?