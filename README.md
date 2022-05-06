# CPSC490

Daniel Ortega's senior project for CPSC 490.

*Insert Demo Video*

# Steps to Run Program

## 0. Install SuperCollider

[Main Page of SuperCollider](https://supercollider.github.io/) (reliable)

[Scott Petersen's Installation Guide](https://www.notion.so/Installing-SuperCollider-613fbb170dff4910bb3b4e024883fbbe) (may or may not be up to date)

## 1. Set up Virtual Environment

`py -m venv 490-venv`
(py, python, python3)

## 2. Activate venv

### Windows

`490-venv\Scripts\activate.bat`

### MacOS/Unix

`source 490-venv/bin/activate`

## 3. Install packages

`python -m pip install pyOSC3`

`python -m pip install pygame`

## 4. Run SuperCollider

Open the SuperCollider IDE, then use it to open `pathfinding.scd`.

Click on any part of the code within parentheses, then press `ctrl + enter` to evaluate the code. Alternatively, look under the `Language` menu for `Evaluate File` or `Evaluate Selection, Line, or Region`. Upon success, you should see `-> localhost` in the bottom right console window.

Note: If you get a server error evaluating the code, try restarting the server by selecting `Server > Kill All Servers` and then `Server > Reboot Server`.

## 5. Run Python

Run `pathfinding.py` in the terminal. This could be via `pathfinding.py`, `py pathfinding.py`, `python pathfinding.py`, etc.

# Keybinds

| Function |  Key | 
| ---- | ------- |
| Start simulation | `space` |
| Switch pathfinding algorithm | `tab` |
| Draw Mode: Place Walls | `1` |
| Draw Mode: Erase Walls | `2` |
| Draw Mode: Place Start | `3` |
| Draw Mode: Place Finish | `4` |
| Draw Mode: Select | `5` |
| Draw Mode: Deselect | `6` |
| Draw Mode: None | `0` |
| Save grid to file | `s` |
| Load grid from file | `l` |
| Generate random grid | `esc` |
| Switch Instruments: Sine Wave | `o` |
| Switch Instruments: Triangle Wave | `p` |
| Edit selected notes | `a`, `b`, `c`, `d`, `e`, `f` |
| Transpose selected notes up | Up Arrow |
| Transpose selected notes down | Down Arrow |
| Clear selection | `del` |


# Steps to Exit Program

## 1. Close pygame window

## 2.  Quit server in SuperCollider 

Press `crtl` + `.`

## 3. Dectivate venv

### Windows/MacOS/Unix

`deactivate`
