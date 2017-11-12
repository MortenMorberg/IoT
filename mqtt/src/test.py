'''
Created on 7. nov. 2017

@author: Andersen
'''

from local.client import Client 
import time
from local.topic import gettopic, gettimediff, getid

topic = 'my/topic'
message = '2'

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(getid(msg.payload))+" "+str(gettimediff(msg.payload, time.time())))

local_client_1 = Client("1", on_message, 'mqtt://localhost:1883')
local_client_2 = Client('2', on_message, 'mqtt://localhost:1883')
local_client_3 = Client('3', on_message, 'mqtt://localhost:1883')

local_client_1.connect()
local_client_2.connect()
local_client_3.connect()

#local_client_1.subscribe(topic)
#local_client_2.subscribe(topic)

#local_client_2.mqttc.loop_start()

local_client_2.consume(200, topic, 0)


local_client_1.produce(10, 1, topic, 0, 1000)
local_client_3.produce(10, 0.5, topic, 0, 10)

while True:
    #local_client_1.produce(10, 1, topic, 0, 10)
    #local_client_2.publish(topic, message)
    time.sleep(1)

