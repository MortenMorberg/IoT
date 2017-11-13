'''
Created on 9. nov. 2017

@author: Andersen
'''

import json
import time

def gettopic(deviceid, msgid, psize):
    timestamp = str(time.time()).ljust(20,'0') #pad zeros to timestamp!
    size_msg = len(json.dumps({"deviceid":deviceid, "msgid":msgid, "Time":timestamp, "Payload":''}))
    return json.dumps({"deviceid":deviceid, "msgid":msgid, "time":timestamp, "payload":''.ljust(psize)})
   
def gettimediff(topic, time):
    msg = json.loads(topic)
    return time - float(msg['Time'])

def getid(topic):
    msg = json.loads(topic)
    return msg['Id']

def getsize(topic):
    return len(topic)
    
