

import sys
import uuid
import time
import json

ls='World'

try:
    import ibmiotf.device
except ImportError as e:
    print(str(e))
    sys.exit()


def myAppEventCallback(event):
    print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.payload)
    
def myEventCallback(event):
    callback_str = "%s event '%s' received from device [%s]: %s"
    print(callback_str % (event.format, event.event, event.device, json.dumps(event.data)))


print       
#####################################
#FILL IN THESE DETAILS
#####################################     
organization = "g9czer"
deviceType = "TestDevice"
deviceId = "TestDevice1"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "123abc123"

# Initialize the device client.
try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print(str(e))
    sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
deviceCli.commandCallback = myCommandCallback

while(1):
    data = {'Hello': ls}
    deviceCli.publishEvent("status", "json", data)
    time.sleep(1)

# Disconnect the device and application from the cloud
deviceCli.disconnect()
#appCli.disconnect()