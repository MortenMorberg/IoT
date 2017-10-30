'''
Created on 27. okt. 2017

@author: Andersen
'''



import sys
import time
import json

import ibmiotf.application

organization = "g9czer"
appId = "myApp"
authMethod = "apikey"
authKey = "a-g9czer-sjjziicpgz"
authToken = "gZ?lyIBndda)1CZGWi"
true = "true"

try:
    options = { 
        "org": organization, 
        "id": appId,
        "auth-method": authMethod, 
        "auth-key": authKey,
        "auth-token": authToken,
        "clean-session": true}
    client = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException  as e:
    print(str(e))
    sys.exit()

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.payload)
    
def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.event, event.device, json.dumps(event.data)))

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
client.connect()
client.commandCallback = myCommandCallback
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents()

while(1):
    #data = {'Hello': 'World'}
    #client.publishEvent("status", "json", data)
    time.sleep(1)

# Disconnect the device and application from the cloud
client.disconnect()
#appCli.disconnect()