'''
Created on 7. nov. 2017

@author: Andersen
'''

from mqttClient import Client 
import time
from topic import gettopic, gettimediff, getid

topic = 'my/topic'
message = '2'

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(getid(msg.payload))+" "+str(gettimediff(msg.payload, time.time())))

local_client_1 = Client("1",'mqtt://localhost:1883')
local_client_2 = Client('2','mqtt://localhost:1883')

local_client_1.connect()
local_client_2.connect()

local_client_1.subscribe(topic={'topic':topic, 'qos':0, 'cb':on_message}, kwargs={'timeout':15})

local_client_2.publish(topic={'topic':topic, 'psize':100, 'qos':0}, kwargs={'nr':10, 'ival':1})

while True:
    time.sleep(1)

