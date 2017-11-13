'''
Created on 9. nov. 2017

@author: Andersen
'''

import json
import time

def gettopic(deviceid, msgid, psize):
    timestamp = str(time.time())
    size_msg = len(json.dumps({"msgid":msgid, "time":timestamp, "payload":''}))
    pad = 60-size_msg
    return json.dumps({"deviceid":deviceid, "msgid":msgid, "time":timestamp, "payload":''.ljust(psize+pad)})
    
def gettimediff(topic, time):
    msg = json.loads(topic)
    return time - float(msg['time'])

def getMsgId(topic):
    msg = json.loads(topic)
    return msg['msgid']

def getsize(topic):
    return len(topic)

def getDeviceId(topic):
    msg = json.loads(topic)
    return msg['deviceid']
    
