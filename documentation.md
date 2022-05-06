## Setting up virtual environment:
py -m venv 490-venv
(py, python, python3)

## Activating venv:

### Windows:
490-venv\Scripts\activate.bat

### MacOS/Unix:
source 490-venv/bin/activate

## Installing packages:
python -m pip install pyOSC3

## Deactivating venv:
deactivate


## OSC Message received by SC in format
message:    [ /print, 440 ]
time:       760.7525028
address:    a NetAddr(127.0.0.1, 55935)
port:       57120

# Log

| Date |  Time   | Log |
| ---- | ------- | --- |
| 2/19 | 2 hours | Going through pygame tutorial https://www.youtube.com/watch?v=FfWpgLFMI7w |
| 2/21 | 5 hours | Add modes for drawing and/or removing walls, start, and finish. Play pitch in OSC according to note on the grid. |
| 2/26 | 5 hours | Play correct pitch according to note. Add visual indication that node was visited over time. |
| 2/28 | 5 hours | Add comments throughout code. Make window scalable. |
| 3/06 | 4 hours | Disallow changes while simulation is running. Add text info on current algorithm and draw mode. Made pluck sound instead of constant tone |
| 3/07 | 4 hours | Stop continuous running (bug fix). Reset rather than have random grid after pathfinding finishes. |
| 3/13 | 5 hours | Add instrument switching. Consolidate the text render into a separate function. Change how algorithm is selected (cycle with Tab instead of individual keys for each). |
| 3/14 | 5 hours | Add selection mode. Add deselection mode. Keybind to clear selection. Type pitch for selected notes = *editable text for each cell!* Transpose up/down with arrow keys. |
| 3/19-3/27 | --- | Spring Break |
| 4/04 | 6 hours | Begin implementation of saving and loading functionality |
| 4/05 | 6 hours | Finish implementing saving and loading functionality |
| 4/11 | 8 hours | Clean up documentation. Define what "sounds good". Experiment to find grid configurations that "sound good". |
| 4/18 | 8 hours | Work on embedding chord progressions and higher level note patterns into the grid which vary on algorithm. |
| 4/25 | 4 hours | Begin final report |
| 4/26 | 3 hours | Continue work on final report |
| 4/29-5/2 | 10 hours | Finish final report |

### What's Next
1. Define what "sounds good"
- Things which could be a melody in a song
- Likely diatonic
- More fifths and fourths than other intervals
2. Define methodology to achieve what sounds good 
3. Screen record prior to meeting
Ideas:

### TODO
1. Clean up variable names
2. Find out which grid setups are meaningful
3. Different grid configurations
4. Higher octaves

### Pending Ideas
- Change color scheme
- Panning based on grid location
- Or panning based on relation to start?
