import pyOSC3
client = pyOSC3.OSCClient()
client.connect( ( '127.0.0.1', 57120 ) )
msg = pyOSC3.OSCMessage()
msg.setAddress("/test")
msg.append(440)
client.send(msg)