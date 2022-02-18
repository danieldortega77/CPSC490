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