'''
Created on 9. nov. 2017

@author: Andersen
'''

import json
import time

def gettopic(topicid, psize):
    timestamp = str(time.time())
    size_msg = len(json.dumps({"Id":topicid, "Time":timestamp, "Payload":''}))
    pad = 60-size_msg
    return json.dumps({"Id":topicid, "Time":timestamp, "Payload":''.ljust(psize+pad)})
    
def gettimediff(topic, time):
    msg = json.loads(topic)
    return time - float(msg['Time'])

def getid(topic):
    msg = json.loads(topic)
    return msg['Id']

def getsize(topic):
    return len(topic)
    